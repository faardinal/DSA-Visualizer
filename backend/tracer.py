"""
Execution tracer using sys.settrace to capture every line execution.
Phase 3.2: Primitive-only serialization.

Captures execution snapshots at each source line with:
- step number
- event type (line, call, return, exception)
- line number
- function name
- locals (primitive values only)
- globals (primitive values only)
- stdout (accumulated print output)
"""
import sys
import time
import io
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .models import ExecutionConfig


@dataclass
class Snapshot:
    """A single execution snapshot."""
    step: int
    event: str  # 'line', 'call', 'return', 'exception'
    line: int
    function: str
    filename: str
    code: str
    locals: Dict[str, Any] = field(default_factory=dict)
    globals: Dict[str, Any] = field(default_factory=dict)
    stdout: str = ""
    exception: Optional[Dict[str, Any]] = None
    heap: Dict[str, Any] = field(default_factory=dict)
    # Unique id of the currently active frame, and the full call stack
    # (innermost last) as [{frame_id, function}]. Lets consumers tell apart
    # recursive calls of the same function, which function-name matching alone
    # cannot do. Backward compatible: consumers that ignore these fields still
    # work off `function` exactly as before.
    frame_id: int = 0
    call_stack: List[Dict[str, Any]] = field(default_factory=list)
    # Only set on 'return' events — the serialized return value of the
    # function that just returned (primitive or {"ref": heap_id}).
    return_value: Any = None
    has_return_value: bool = False


def serialize_value(value: Any) -> Any:
    """
    Serialize a value for the trace.
    Only primitive types are serialized directly.
    Non-primitive types return {"type": "unsupported"}.
    """
    # Primitive types that can be safely serialized
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        # Check for special float values
        if isinstance(value, float) and (value != value or value == float('inf') or value == float('-inf')):
            return {"type": "unsupported"}
        return value
    if isinstance(value, str):
        return value
    
    # Everything else is unsupported in Phase 3.2
    return {"type": "unsupported"}


def serialize_locals(frame_locals: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize local variables, only keeping primitive values."""
    result = {}
    for name, value in frame_locals.items():
        # Skip internal/dunder variables
        if name.startswith('__') and name.endswith('__'):
            continue
        result[name] = serialize_value(value)
    return result


def serialize_globals(frame_globals: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize global variables, only keeping primitive values."""
    result = {}
    for name, value in frame_globals.items():
        # Skip internal/dunder variables
        if name.startswith('__') and name.endswith('__'):
            continue
        # Skip modules, functions, classes, types
        if isinstance(value, (type, type(sys), type(io.StringIO))):
            continue
        if callable(value):
            continue
        result[name] = serialize_value(value)
    return result


def _is_primitive(value: Any) -> bool:
    return value is None or isinstance(value, (bool, int, float, str))


class ExecutionTracer:
    """
    Traces Python execution using sys.settrace.
    Captures line executions, function calls/returns, and exceptions.
    Only serializes primitive values (int, float, bool, str, None).
    """

    class _StopExecution(Exception):
        pass

    def __init__(self, config: Optional[ExecutionConfig] = None):
        self.config = config or ExecutionConfig()
        self.snapshots: List[Snapshot] = []
        self.step_counter = 0
        self.start_time = 0.0
        self.stdout_buffer = io.StringIO()
        
        # Frame tracking
        self._call_stack: List[Dict] = []  # Stack of {func_name, filename, line, frame_id}
        self._next_frame_id = 0
        self._source_code: str = ""
        self._source_lines: List[str] = []
        
        # Tracking for deduplication
        self._last_line: Optional[int] = None
        self._last_filename: Optional[str] = None
        
        # Exception tracking
        self._error: Optional[str] = None
        # Machine-readable category for `_error`, additive alongside the
        # human-readable string so the frontend can render distinct UI per
        # failure kind without parsing message text. One of: "syntax_error",
        # "runtime_error", "step_limit", "time_limit", "recursion_limit".
        self._error_type: Optional[str] = None
        self._exception_info: Optional[Dict] = None
        self._stopped = False
        # Stable heap id mapping for this execution (maps Python id(obj) -> small int)
        self._obj_id_map: Dict[int, int] = {}
        self._next_heap_id = 0
        # Reverse mapping: heap id -> actual object (to materialize into snapshots)
        self._heap_objs: Dict[int, Any] = {}
        

    def _stop_execution(self, message: str, error_type: str = "runtime_error"):
        self._error = message
        self._error_type = error_type
        self._stopped = True
        raise self._StopExecution(message)

    def _get_source_line(self, line_no: int) -> str:
        """Get source code line by number."""
        if 1 <= line_no <= len(self._source_lines):
            return self._source_lines[line_no - 1].rstrip()
        return f"# Line {line_no}"

    def _should_skip_frame(self, filename: str, func_name: str) -> bool:
        """Determine if a frame should be skipped (internal/system frames)."""
        # Skip library frames (but NOT user code which uses <user_code> filename)
        if 'site-packages' in filename or 'dist-packages' in filename:
            return True
        # Skip tracer's own frames
        if 'tracer.py' in filename:
            return True
        # Skip built-in frames like <frozen importlib>, <string> (but allow <user_code>)
        if filename.startswith('<') and filename.endswith('>') and filename != '<user_code>':
            return True
        return False

    def _check_limits(self) -> bool:
        """Check if execution limits have been exceeded."""
        # Recursion depth only (step/time handled in trace_function for speed)
        if len(self._call_stack) >= self.config.max_recursion_depth:
            self._error = f"Recursion depth limit exceeded ({self.config.max_recursion_depth})"
            self._error_type = "recursion_limit"
            return True
        return False

    # Heap serialization helpers
    def _reset_heap(self):
        self._obj_id_map = {}
        self._next_heap_id = 0
        self._heap_objs = {}

    def _assign_heap_id(self, obj: Any) -> int:
        oid = id(obj)
        if oid in self._obj_id_map:
            return self._obj_id_map[oid]
        self._next_heap_id += 1
        self._obj_id_map[oid] = self._next_heap_id
        self._heap_objs[self._next_heap_id] = obj
        return self._next_heap_id

    def _serialize_value_with_heap(self, value: Any, heap: Dict[int, Any], visited: set):
        # Primitives serialized directly
        if _is_primitive(value):
            return value

        oid = id(value)

        # If already assigned a heap id, ensure it's materialized into this snapshot's heap
        if oid in self._obj_id_map:
            hid = self._obj_id_map[oid]
            if hid not in heap:
                # materialize into this snapshot's heap
                self._materialize_heap_entry(hid, value, heap, visited)
            return {"ref": hid}

        # Prevent infinite recursion
        if oid in visited:
            hid = self._obj_id_map.get(oid) or self._assign_heap_id(value)
            if hid not in heap:
                self._materialize_heap_entry(hid, value, heap, visited)
            return {"ref": hid}

        # Assign stable heap id
        hid = self._assign_heap_id(value)
        visited.add(oid)

        # Create entry now
        self._materialize_heap_entry(hid, value, heap, visited)
        return {"ref": hid}

    def _materialize_heap_entry(self, hid: int, value: Any, heap: Dict[int, Any], visited: set):
        # Avoid re-materializing
        if hid in heap:
            return

        # Guard against unbounded heap growth (huge/generative data structures)
        # rather than letting the process run out of memory. Once the cap is
        # hit, remaining objects are represented as a lightweight stub instead
        # of crashing the whole execution.
        if len(self._heap_objs) > self.config.max_heap_objects:
            heap[hid] = {"type": "unsupported", "reason": "heap_limit_exceeded"}
            return

        # Any single malformed/exotic object (e.g. a property that raises,
        # a broken __iter__, an uncopyable descriptor) must not take down the
        # whole trace — fall back to a generic "unsupported" stub for it and
        # keep going, per the Phase 3 "never crash" requirement.
        try:
            self._materialize_heap_entry_inner(hid, value, heap, visited)
        except Exception as exc:
            heap[hid] = {"type": "unsupported", "reason": str(exc)[:200]}

    def _materialize_heap_entry_inner(self, hid: int, value: Any, heap: Dict[int, Any], visited: set):
        # Pre-create a placeholder to allow recursive references back to this object.
        if isinstance(value, list):
            heap[hid] = {"type": "list", "elements": []}
            elements = [self._serialize_value_with_heap(e, heap, visited) for e in value]
            heap[hid]["elements"] = elements
            return
        if isinstance(value, tuple):
            heap[hid] = {"type": "tuple", "elements": []}
            elements = [self._serialize_value_with_heap(e, heap, visited) for e in value]
            heap[hid]["elements"] = elements
            return
        if isinstance(value, set):
            heap[hid] = {"type": "set", "elements": []}
            elements = [self._serialize_value_with_heap(e, heap, visited) for e in value]
            heap[hid]["elements"] = elements
            return
        if isinstance(value, dict):
            heap[hid] = {"type": "dict", "entries": []}
            entries = []
            for k, v in value.items():
                try:
                    key_ser = k if _is_primitive(k) else self._serialize_value_with_heap(k, heap, visited)
                    val_ser = self._serialize_value_with_heap(v, heap, visited)
                    entries.append([key_ser, val_ser])
                except Exception:
                    continue
            heap[hid]["entries"] = entries
            return
        attrs = getattr(value, '__dict__', None)
        if isinstance(attrs, dict):
            heap[hid] = {"type": value.__class__.__name__, "attributes": {}}
            attributes = {}
            for k, v in attrs.items():
                try:
                    attributes[k] = self._serialize_value_with_heap(v, heap, visited)
                except Exception:
                    attributes[k] = {"type": "unsupported"}
            heap[hid]["attributes"] = attributes
            return
        # Generators, iterators, and other exotic types: represent them as a
        # readable stub rather than crashing (consuming a generator here
        # would also change program behavior, which we must never do).
        heap[hid] = {"type": "unsupported", "class_name": type(value).__name__}
    
    def trace_function(self, frame, event, arg):
        """Main trace function called by sys.settrace."""
        # Check if we should stop
        if self._stopped:
            return None

        # Count every traced event, even if it does not create a snapshot.
        self.step_counter += 1

        # Fast step-limit check (avoid time.time() call on every traced event)
        if self.step_counter >= self.config.max_steps:
            self._stop_execution(f"Step limit exceeded ({self.config.max_steps})", "step_limit")

        # Time limit check (less frequent)
        if self.step_counter % 500 == 0:
            if time.time() - self.start_time > self.config.max_time_seconds:
                self._stop_execution(f"Execution time limit exceeded ({self.config.max_time_seconds}s)", "time_limit")

        filename = frame.f_code.co_filename
        line_no = frame.f_lineno
        func_name = frame.f_code.co_name

        # Skip internal frames
        if self._should_skip_frame(filename, func_name):
            return self.trace_function

        # Handle different events
        if event == 'call':
            return self._handle_call(frame, func_name, filename, line_no)
        elif event == 'line':
            return self._handle_line(frame, filename, line_no)
        elif event == 'return':
            return self._handle_return(frame, func_name, filename, line_no, arg)
        elif event == 'exception':
            return self._handle_exception(frame, arg)

        return self.trace_function
    

    def _handle_call(self, frame, func_name: str, filename: str, line_no: int):
        """Handle function call event."""
        # Push onto call stack. Each call gets a unique frame_id so that
        # recursive calls of the same function can be told apart (the
        # frontend can no longer rely on function-name matching alone).
        self._next_frame_id += 1
        self._call_stack.append({
            'func_name': func_name,
            'filename': filename,
            'line': line_no,
            'frame_id': self._next_frame_id,
        })

        # Enforce recursion depth limit immediately after pushing the new frame.
        if self._check_limits():
            self._stop_execution(self._error, self._error_type or "recursion_limit")

        return self.trace_function

    def _handle_line(self, frame, filename: str, line_no: int):
        """Handle line execution event."""
        # Skip if same line in same file (deduplication)
        if line_no == self._last_line and filename == self._last_filename:
            return self.trace_function

        self._last_line = line_no
        self._last_filename = filename

        # Get current function name from call stack
        func_name = self._call_stack[-1]['func_name'] if self._call_stack else '<module>'
        code = self._get_source_line(line_no)

        # Create snapshot
        self._create_snapshot('line', line_no, func_name, filename, code, frame)

        return self.trace_function

    def _handle_return(self, frame, func_name: str, filename: str, line_no: int, return_value: Any):
        """Handle function return event."""
        if not self._call_stack:
            return self.trace_function

        # Snapshot the stack (including the returning frame) BEFORE popping,
        # so the return event still reports the frame that is exiting.
        func_name = self._call_stack[-1]['func_name']
        code = self._get_source_line(line_no)

        # Create return snapshot
        self._create_snapshot('return', line_no, func_name, filename, code, frame, return_value)

        # Now pop from call stack
        self._call_stack.pop()

        return self.trace_function

    def _handle_exception(self, frame, arg):
        """Handle exception event."""
        exc_type, exc_value, exc_tb = arg
        self._exception_info = {
            'type': exc_type.__name__,
            'message': str(exc_value),
            'line': frame.f_lineno
        }

        filename = frame.f_code.co_filename
        line_no = frame.f_lineno
        func_name = self._call_stack[-1]['func_name'] if self._call_stack else '<module>'
        code = self._get_source_line(line_no)

        # Create exception snapshot
        self._create_snapshot('exception', line_no, func_name, filename, code, frame, 
                             exception=self._exception_info)

        return self.trace_function

    def _create_snapshot(self, event: str, line_no: int, func_name: str, 
                        filename: str, code: str, frame, 
                        return_value: Any = None,
                        exception: Optional[Dict] = None):
        """Create a snapshot of current execution state."""
        # HARD STOP: do not perform any serialization or allocation after max_steps.
        # `step_counter` is the single source of truth, incremented once per
        # traced event in `trace_function` — no second increment here, so the
        # configured `max_steps` maps directly to the number of traced events
        # rather than being consumed twice as fast.
        if self.step_counter >= self.config.max_steps:
            if not self._error:
                self._error = f"Step limit exceeded ({self.config.max_steps})"
                self._error_type = "step_limit"
            self._stopped = True
            return

        # Prepare heap for this snapshot. Use the per-execution stable id mapping.
        heap: Dict[int, Any] = {}
        visited = set()

        # Phase 3.3: locals serialize primitives directly, non-primitives as heap refs.
        # A single local that fails to serialize (exotic object, broken
        # descriptor, etc.) must not abort the whole snapshot.
        locals_dict: Dict[str, Any] = {}
        for name, val in frame.f_locals.items():
            if name.startswith('__') and name.endswith('__'):
                continue
            # Skip modules, classes/types, and functions — same filter already
            # applied to globals below. Without this, `import heapq` (or any
            # module-level `import`) at module scope makes the imported module
            # itself a local (module code runs with locals is globals), and
            # walking a stdlib module's __dict__ pulls in the entire builtins
            # module transitively, ballooning the heap to thousands of
            # unrelated entries for a plain `import` statement.
            if isinstance(val, (type, type(sys), type(io.StringIO))):
                continue
            if callable(val):
                continue
            try:
                locals_dict[name] = self._serialize_value_with_heap(val, heap, visited)
            except Exception:
                locals_dict[name] = {"type": "unsupported"}


        # Phase 3.3: globals serialize primitives directly, non-primitives as heap refs
        globals_dict: Dict[str, Any] = {}
        if func_name == '<module>':
            for name, val in frame.f_globals.items():
                if name.startswith('__') and name.endswith('__'):
                    continue
                if isinstance(val, (type, type(sys), type(io.StringIO))):
                    continue
                if callable(val):
                    continue
                try:
                    globals_dict[name] = self._serialize_value_with_heap(val, heap, visited)
                except Exception:
                    globals_dict[name] = {"type": "unsupported"}


        # Phase 3.4: serialize the return value (only meaningful on 'return' events)
        serialized_return_value = None
        has_return_value = False
        if event == 'return':
            try:
                serialized_return_value = self._serialize_value_with_heap(return_value, heap, visited)
            except Exception:
                serialized_return_value = {"type": "unsupported"}
            has_return_value = True

        # Ensure all known heap objects are materialized into this snapshot
        for hid, obj in self._heap_objs.items():
            if hid not in heap:
                # materialize missing entries into the heap
                self._materialize_heap_entry(hid, obj, heap, visited)

        # Convert heap keys to strings for JSON stability. No deepcopy needed:
        # every entry in `heap` was freshly built from scratch by
        # `_materialize_heap_entry_inner` (new dicts/lists of serialized
        # values), never a view into the live traced objects, so snapshot
        # immutability already holds without an extra copy pass.
        snapshot_heap: Dict[str, Any] = {str(k): v for k, v in heap.items()}

        # Get stdout
        stdout_content = self.stdout_buffer.getvalue()

        current_frame_id = self._call_stack[-1]['frame_id'] if self._call_stack else 0
        call_stack_snapshot = [
            {'frame_id': f['frame_id'], 'function': f['func_name']}
            for f in self._call_stack
        ]

        snapshot = Snapshot(
            step=self.step_counter,
            event=event,
            line=line_no,
            function=func_name,
            filename=filename,
            code=code,
            locals=locals_dict,
            globals=globals_dict,
            stdout=stdout_content,
            exception=exception,
            heap=snapshot_heap,
            frame_id=current_frame_id,
            call_stack=call_stack_snapshot,
            return_value=serialized_return_value,
            has_return_value=has_return_value,
        )

        # Append immutable snapshot (heap dict values are simple structures)
        self.snapshots.append(snapshot)

    def execute(self, code: str, inputs: str = "") -> tuple:
        """
        Execute code and return snapshots.
        Returns (snapshots_list, error_message, execution_time)
        """
        self.start_time = time.time()
        self.snapshots = []
        self.step_counter = 0
        self._call_stack = []
        self._next_frame_id = 0
        self._last_line = None
        self._last_filename = None
        self._error = None
        self._exception_info = None
        self._stopped = False
        self._source_code = code
        self._source_lines = code.splitlines()
        # Reset stable heap id mapping for this execution
        self._reset_heap()

        # Compile code
        try:
            compiled_code = compile(code, '<user_code>', 'exec')
        except SyntaxError as e:
            self._error = f"Syntax error: {e}"
            self._error_type = "syntax_error"
            return [], self._error, 0.0, self._error_type

        # Set up tracing
        old_trace = sys.gettrace()
        sys.settrace(self.trace_function)

        # Redirect stdout
        old_stdout = sys.stdout
        sys.stdout = self.stdout_buffer

        # Prepare input if provided
        old_stdin = None
        if inputs:
            old_stdin = sys.stdin
            sys.stdin = io.StringIO(inputs)

        try:
            # Create a clean global namespace
            global_ns = {
                '__name__': '__main__',
                '__doc__': None,
                '__builtins__': __builtins__,
            }
            
            # Execute
            exec(compiled_code, global_ns)
        except self._StopExecution:
            # Execution stopped by tracer due to limit breach.
            pass
        except Exception as e:
            if not self._error:
                self._error = f"Runtime error: {type(e).__name__}: {e}"
                self._error_type = "runtime_error"
        finally:
            # Restore
            sys.settrace(old_trace)
            sys.stdout = old_stdout
            if old_stdin:
                sys.stdin = old_stdin

        execution_time = time.time() - self.start_time

        return self.snapshots, self._error, execution_time, self._error_type


def execute_python(code: str, inputs: str = "", config: Optional[ExecutionConfig] = None) -> tuple:
    """
    High-level function to execute Python code and get snapshots.
    Returns (snapshots_list, error, execution_time, error_type)
    """
    tracer = ExecutionTracer(config)
    return tracer.execute(code, inputs)