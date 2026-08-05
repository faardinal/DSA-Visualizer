"""
Main execution orchestrator for the LeetCode-style execution engine.

Takes user source code, parses it, resolves the problem plugin (or
auto-configures from type hints), generates wrapper code, executes via
the existing tracer, validates output, and returns structured results
with a visualization trace.

This module is the SINGLE entry point for the execution engine.
It coordinates parser → registry → wrapper generator → tracer → validators.
It never knows about React, rendering, or the frontend.
"""

import json
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

from .errors import (
    EngineError,
    NoSolutionClassError,
    ParseError,
    SecurityViolationError,
    AmbiguousMethodError,
    classify_error,
)
from .parser import parse_source, has_solution_class, ParsedSolution, MethodInfo
from .plugin_base import (
    ProblemPlugin, ProblemInfo, TestCase, ValidationResult,
)
from .plugin_registry import get_registry, PluginRegistry
from .security import sanitize_source
from .wrapper_generator import generate_wrapper
from .validators import validator_for


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TestCaseResult:
    """Result of executing a single test case."""
    test_idx: int
    description: str
    passed: bool
    expected: Any = None
    actual: Any = None
    input_repr: str = ""
    console_output: str = ""
    exception: Optional[str] = None
    traceback: Optional[str] = None
    execution_time: float = 0.0
    memory_bytes: Optional[int] = None
    # Internal: snapshots captured for trace extraction (not serialized)
    _snapshots: list = field(default_factory=list, repr=False, compare=False)

    def to_dict(self) -> dict:
        return {
            "test_idx": self.test_idx,
            "description": self.description,
            "passed": self.passed,
            "expected": self.expected,
            "actual": self.actual,
            "input_repr": self.input_repr,
            "console_output": self.console_output,
            "exception": self.exception,
            "traceback": self.traceback,
            "execution_time": self.execution_time,
            "memory_bytes": self.memory_bytes,
        }


@dataclass
class ExecutionStats:
    """Aggregate statistics across all test cases."""
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    pass_percentage: float = 0.0
    avg_runtime: float = 0.0
    worst_runtime: float = 0.0
    fastest_runtime: float = 0.0
    total_memory: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "pass_percentage": self.pass_percentage,
            "avg_runtime": self.avg_runtime,
            "worst_runtime": self.worst_runtime,
            "fastest_runtime": self.fastest_runtime,
            "total_memory": self.total_memory,
        }


@dataclass
class ExecutionResult:
    """Complete result of running a LeetCode solution."""
    passed: bool = False
    test_results: list = field(default_factory=list)
    total_time: float = 0.0
    method_detected: str = ""
    problem_id: Optional[str] = None
    problem_title: Optional[str] = None
    ambiguous_problems: Optional[list] = None
    trace: list = field(default_factory=list)
    trace_test_idx: int = 0
    error: Optional[str] = None
    error_type: Optional[str] = None
    statistics: Optional[ExecutionStats] = None

    def to_dict(self) -> dict:
        result = {
            "success": self.error is None and len(self.ambiguous_problems or []) == 0,
            "passed": self.passed,
            "test_results": [r.to_dict() for r in self.test_results],
            "statistics": self.statistics.to_dict() if self.statistics else None,
            "method_detected": self.method_detected,
            "problem_id": self.problem_id,
            "problem_title": self.problem_title,
            "trace": self.trace,
            "trace_test_idx": self.trace_test_idx,
            "total_time": self.total_time,
            "execution_time": self.total_time,
        }
        if self.error:
            result["error"] = self.error
            result["error_type"] = self.error_type
        if self.ambiguous_problems:
            result["ambiguous_problems"] = self.ambiguous_problems
            result["error"] = self.error
            result["error_type"] = self.error_type
        return result


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_solution(
    source_code: str,
    problem_id: Optional[str] = None,
    method_name: Optional[str] = None,
    replay_test_idx: Optional[int] = None,
    config=None,
) -> ExecutionResult:
    """
    Execute a LeetCode-style solution and return structured results.

    Args:
        source_code: The user's Python source code (must contain class Solution).
        problem_id: Optional explicit problem ID (bypasses auto-detection).
        method_name: Optional method name hint (used if no problem_id).
        replay_test_idx: If specified, generate trace for this test case only.
        config: Optional ExecutionConfig for the tracer.

    Returns:
        ExecutionResult with test results, trace, statistics, and error info.
    """
    start_time = time.time()

    # --- Step 1: Security check ---
    try:
        sanitize_source(source_code)
    except SecurityViolationError as e:
        return ExecutionResult(
            error=str(e),
            error_type="security_violation",
            total_time=time.time() - start_time,
        )

    # --- Step 2: Parse source ---
    try:
        parsed = parse_source(source_code)
    except (NoSolutionClassError, ParseError) as e:
        return ExecutionResult(
            error=str(e),
            error_type="parse_error" if isinstance(e, ParseError) else "no_solution",
            total_time=time.time() - start_time,
        )

    # --- Step 3: Resolve the problem plugin ---
    registry = get_registry()
    plugin = None
    method = None
    ambiguous = None

    if problem_id:
        plugin = registry.get(problem_id)
        if plugin is None:
            return ExecutionResult(
                error=f"Problem '{problem_id}' not found in registry.",
                error_type="plugin_not_found",
                total_time=time.time() - start_time,
            )
        method = _find_method(parsed, plugin.method_name)

    elif method_name:
        matches = registry.find_by_method(method_name)
        if len(matches) > 1:
            ambiguous = [m.to_info().to_dict() for m in matches]
            return ExecutionResult(
                ambiguous_problems=ambiguous,
                error=f"Multiple problems match method '{method_name}'. Please select one.",
                error_type="ambiguous_method",
                method_detected=method_name,
                total_time=time.time() - start_time,
            )
        elif len(matches) == 1:
            plugin = matches[0]
            method = _find_method(parsed, plugin.method_name)
        else:
            # No plugin match — auto-configure from type hints
            method = _find_method(parsed, method_name)

    else:
        # Auto-detect: try to find a plugin by the single method
        if len(parsed.methods) == 1:
            method = parsed.methods[0]
            matches = registry.find_by_method(method.name)
            if len(matches) > 1:
                ambiguous = [m.to_info().to_dict() for m in matches]
                return ExecutionResult(
                    ambiguous_problems=ambiguous,
                    error=f"Multiple problems match method '{method.name}'. Please select one.",
                    error_type="ambiguous_method",
                    method_detected=method.name,
                    total_time=time.time() - start_time,
                )
            elif len(matches) == 1:
                plugin = matches[0]
        else:
            # Multiple methods — can't auto-detect
            method_names = [m.name for m in parsed.methods]
            return ExecutionResult(
                error=f"Multiple methods found ({', '.join(method_names)}). "
                      f"Please specify a method or problem_id.",
                error_type="ambiguous_method",
                method_detected="",
                total_time=time.time() - start_time,
            )

    if method is None:
        return ExecutionResult(
            error="Could not find the target method in the Solution class.",
            error_type="method_not_found",
            total_time=time.time() - start_time,
        )

    # --- Step 4: Get test cases ---
    test_cases = []
    if plugin:
        test_cases = plugin.get_test_cases()
    else:
        # Generate basic tests from type hints
        test_cases = _generate_basic_tests(method)

    if not test_cases:
        return ExecutionResult(
            error="No test cases available for this problem.",
            error_type="no_tests",
            total_time=time.time() - start_time,
        )

    # --- Step 5: Execute each test case ---
    validator = plugin.get_validator() if plugin else None
    test_results = []
    all_traces = []  # (test_idx, snapshots)
    passed_count = 0
    runtimes = []

    for idx, tc in enumerate(test_cases):
        tc_result = _execute_single_test(
            source_code=source_code,
            parsed=parsed,
            plugin=plugin,
            test_case=tc,
            method=method,
            validator=validator,
            test_idx=idx,
            config=config,
            capture_trace=(replay_test_idx is not None and idx == replay_test_idx)
                          or (replay_test_idx is None and idx == 0),
        )
        test_results.append(tc_result)
        all_traces.append((idx, tc_result._snapshots))
        runtimes.append(tc_result.execution_time)
        if tc_result.passed:
            passed_count += 1

    # --- Step 6: Build statistics ---
    stats = _build_stats(test_results, runtimes)

    # --- Step 7: Select trace ---
    trace = []
    trace_idx = 0
    if replay_test_idx is not None:
        trace_idx = replay_test_idx
    for idx, snapshots in all_traces:
        if idx == trace_idx and snapshots:
            from backend.tracer import Snapshot
            trace = [_snapshot_to_dict(s) for s in snapshots]
            break

    total_time = time.time() - start_time

    return ExecutionResult(
        passed=passed_count == len(test_cases),
        test_results=test_results,
        total_time=total_time,
        method_detected=method.name,
        problem_id=plugin.problem_id if plugin else None,
        problem_title=plugin.title if plugin else None,
        trace=trace,
        trace_test_idx=trace_idx,
        statistics=stats,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _find_method(parsed: ParsedSolution, method_name: str) -> Optional[MethodInfo]:
    """Find a method by name in the parsed solution."""
    for m in parsed.methods:
        if m.name == method_name:
            return m
    return None


def _execute_single_test(
    source_code: str,
    parsed: ParsedSolution,
    plugin: Optional[ProblemPlugin],
    test_case: TestCase,
    method: MethodInfo,
    validator,
    test_idx: int,
    config=None,
    capture_trace: bool = False,
) -> TestCaseResult:
    """Execute a single test case and return the result."""
    exec_start = time.time()

    # Generate wrapper
    try:
        wrapper_code = generate_wrapper(source_code, parsed, plugin, test_case, method)
    except Exception as e:
        return TestCaseResult(
            test_idx=test_idx,
            description=test_case.description,
            passed=False,
            input_repr=test_case.input_repr(),
            exception=f"Wrapper generation error: {e}",
            traceback=traceback.format_exc(),
            execution_time=time.time() - exec_start,
        )

    # Execute via the existing tracer
    snapshots = []
    exec_error = None
    exec_error_type = None
    stdout_content = ""

    try:
        from backend.tracer import execute_python
        snapshots, exec_error, exec_time, exec_error_type = execute_python(
            wrapper_code, "", config
        )
        # Collect stdout from last snapshot
        if snapshots:
            stdout_content = snapshots[-1].stdout or ""
    except Exception as e:
        error_type, message = classify_error(e)
        return TestCaseResult(
            test_idx=test_idx,
            description=test_case.description,
            passed=False,
            input_repr=test_case.input_repr(),
            exception=message,
            traceback=traceback.format_exc(),
            execution_time=time.time() - exec_start,
        )

    exec_time = time.time() - exec_start

    # Parse execution result from stdout markers
    result_value = None
    console_output = ""

    if exec_error:
        return TestCaseResult(
            test_idx=test_idx,
            description=test_case.description,
            passed=False,
            input_repr=test_case.input_repr(),
            console_output=console_output,
            exception=exec_error,
            execution_time=exec_time,
        )

    # Parse __RESULT__ from stdout
    try:
        result_value, console_output = _parse_result_markers(stdout_content)
    except Exception:
        pass

    # Validate
    passed = False
    expected = test_case.expected

    if validator and result_value is not None:
        try:
            validation: ValidationResult = validator.validate(result_value, expected)
            passed = validation.passed
        except Exception as e:
            passed = False
    elif result_value is not None:
        passed = (result_value == expected)

    result = TestCaseResult(
        test_idx=test_idx,
        description=test_case.description,
        passed=passed,
        expected=expected,
        actual=result_value,
        input_repr=test_case.input_repr(),
        console_output=console_output,
        execution_time=exec_time,
    )

    # Store snapshots on the result object for later trace extraction
    result._snapshots = snapshots if capture_trace else []

    return result


def _parse_result_markers(stdout: str) -> tuple:
    if not stdout:
        return None, ""

    result_value = None
    console_output = ""

    lines = stdout.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line == "__RESULT__:":
            # Next non-empty lines until next marker are the result
            result_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("__"):
                result_lines.append(lines[i])
                i += 1
            result_str = "\n".join(result_lines).strip()
            if result_str:
                try:
                    result_value = json.loads(result_str)
                except (json.JSONDecodeError, ValueError):
                    try:
                        result_value = eval(result_str)
                    except Exception:
                        result_value = result_str
            continue

        if line == "__CONSOLE__:":
            console_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("__"):
                console_lines.append(lines[i])
                i += 1
            console_output = "\n".join(console_lines)
            continue

        i += 1

    return result_value, console_output


def _generate_basic_tests(method: MethodInfo) -> list:
    """Generate basic test cases from method type hints when no plugin matches."""
    tests = []
    # Create one test case with placeholder values based on param types
    inputs = {}
    for param in method.params:
        ann_str = param.annotation_str.lower() if param.annotation_str else ""
        if "list" in ann_str:
            inputs[param.name] = [1, 2, 3]
        elif "str" in ann_str:
            inputs[param.name] = "abc"
        elif "int" in ann_str:
            inputs[param.name] = 42
        elif "float" in ann_str:
            inputs[param.name] = 1.0
        elif "bool" in ann_str:
            inputs[param.name] = True
        elif "tree" in ann_str:
            inputs[param.name] = [1, 2, 3]
        elif "listnode" in ann_str or "linked" in ann_str:
            inputs[param.name] = [1, 2, 3]
        else:
            inputs[param.name] = 0

    tests.append(TestCase(
        inputs=inputs,
        expected=None,
        description="Auto-generated test (no plugin matched)",
        is_hidden=False,
    ))
    return tests


def _build_stats(test_results: list, runtimes: list) -> ExecutionStats:
    """Build aggregate statistics from test results."""
    total = len(test_results)
    passed = sum(1 for r in test_results if r.passed)
    failed = total - passed

    if runtimes:
        avg = sum(runtimes) / len(runtimes)
        worst = max(runtimes)
        fastest = min(runtimes)
    else:
        avg = worst = fastest = 0.0

    return ExecutionStats(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        pass_percentage=round((passed / total * 100) if total > 0 else 0, 1),
        avg_runtime=round(avg, 6),
        worst_runtime=round(worst, 6),
        fastest_runtime=round(fastest, 6),
    )


def _snapshot_to_dict(snapshot) -> dict:
    """Convert a Snapshot dataclass to dict for JSON serialization."""
    result = {
        "step": snapshot.step,
        "event": snapshot.event,
        "line": snapshot.line,
        "function": snapshot.function,
        "code": snapshot.code,
        "locals": snapshot.locals,
        "globals": snapshot.globals,
        "stdout": snapshot.stdout,
        "heap": snapshot.heap,
        "frame_id": snapshot.frame_id,
        "call_stack": snapshot.call_stack,
    }
    if snapshot.exception:
        result["exception"] = snapshot.exception
    if snapshot.has_return_value:
        result["return_value"] = snapshot.return_value
    return result
