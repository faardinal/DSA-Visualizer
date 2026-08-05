# LeetCode Execution Engine

A plugin-based, language-agnostic execution engine that runs user-submitted
`class Solution` code against hidden test cases and produces standardized
events for the visualization frontend.

**Execution and visualization are fully decoupled.** This engine only knows
how to *run* code and *emit events*. The frontend consumes those events via
`adaptBackendTrace()` — neither side knows the other's internals.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        run_solution(code, …)                     │
│                          (runner.py — orchestrator)              │
│                                                                  │
│  1. security.sanitize_source   ──►  AST scan, reject unsafe code │
│  2. parser.parse_source        ──►  ParsedSolution (class+method)│
│  3. registry.resolve(plugin?)  ──►  ProblemPlugin (or ambiguous) │
│  4. for each TestCase:                                            │
│       a. wrapper_generator.generate_wrapper(...)                  │
│       b. tracer.execute_python(wrapper)  ──► snapshots + stdout  │
│       c. parse __RESULT__: markers from stdout                    │
│       d. validator.validate(actual, expected)                     │
│       e. build TestCaseResult                                     │
│  5. aggregate ExecutionStats, pick trace (replay idx or first)    │
│  6. return ExecutionResult                                        │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼  (JSON over HTTP)
┌──────────────────────────────────────────────────────────────────┐
│              POST /api/run-solution   (backend/routes.py)         │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Frontend (React)                               │
│   runSolution.js → adaptSolutionTrace.js → diffEngine → renderers│
│   TestResultsPanel.jsx  (pass/fail, replay failed test)          │
└──────────────────────────────────────────────────────────────────┘
```

### Module map

| Module | Responsibility |
|---|---|
| `runner.py` | Orchestrator. `run_solution()` is the only entry point. |
| `parser.py` | AST-based `parse_source()` → `ParsedSolution`, `MethodInfo`. |
| `type_hints.py` | `parse_type_hint()` for `List[int]`, `Optional[TreeNode]`, etc. |
| `plugin_base.py` | `ProblemPlugin` ABC + `TestCase`, `Validator`, `WrapperTemplate`. |
| `plugin_registry.py` | Discovers plugins from `problems/*.py`. Handles ambiguity. |
| `object_builder.py` | `ListNode`/`TreeNode`/`TrieNode` builders + serializers. |
| `wrapper_generator.py` | Template-based wrapper generation per DSA pattern. |
| `validators.py` | 10 validators: Equality, Unordered, FloatTolerance, Tree, … |
| `random_generator.py` | Optional random test generation per pattern. |
| `security.py` | AST-based source sanitizer. Blocks `os`, `sys`, `eval`, … |
| `errors.py` | Exception hierarchy + `classify_error()` for 15+ types. |
| `problems/` | One file per problem. Drop a file → it's registered. |

---

## Public API

### Python

```python
from backend.execution_engine import run_solution, list_problems, get_registry

result = run_solution(
    source_code,                # str: user's `class Solution: ...`
    problem_id='two-sum',       # str?  explicit problem
    method_name=None,           # str?  fallback if problem_id absent
    replay_test_idx=None,       # int?  capture full trace for this test
    config=None,                # ExecutionConfig?  limits override
)
# → ExecutionResult with .passed, .test_results, .statistics, .trace, ...
```

### HTTP

| Method | Path | Body / Query | Returns |
|---|---|---|---|
| `POST` | `/api/run-solution` | `{code, problem_id?, method?, replay_test_idx?, config?}` | `ExecutionResult.to_dict()` |
| `GET`  | `/api/problems` | — | `{problems: [{problem_id, title, difficulty, pattern, …}]}` |
| `POST` | `/api/run` | `{code, config?}` | (unchanged) free-form trace |
| `GET`  | `/api/health`, `/api/config` | — | (unchanged) |

---

## `ExecutionResult` shape

```jsonc
{
  "passed": true,                       // overall pass
  "method_detected": "twoSum",
  "problem_id": "two-sum",
  "problem_title": "Two Sum",
  "ambiguous_problems": [],             // non-empty when ambiguous
  "error": null, "error_type": null,
  "trace": [ /* snapshots, for replay_test_idx or test 0 */ ],
  "trace_test_idx": 0,
  "statistics": {
    "total_tests": 6, "passed_tests": 6, "failed_tests": 0,
    "pass_percentage": 100.0,
    "avg_runtime": 0.00031, "worst_runtime": 0.0006, "fastest_runtime": 0.0002,
    "total_memory": 12000
  },
  "test_results": [
    {
      "test_idx": 0, "description": "...", "passed": true,
      "input_repr": "nums = [2, 7, 11, 15]\ntarget = 9",
      "expected": "[0, 1]", "actual": "[0, 1]",
      "console_output": "", "exception": null, "traceback": null,
      "execution_time": 0.0003, "memory_bytes": 2000
    }
  ]
}
```

---

## Adding a new problem (3 minutes)

Create **one file**: `backend/execution_engine/problems/my_problem.py`.

```python
from ..plugin_base import ProblemPlugin, TestCase
from ..validators import EqualityValidator

class MyProblem(ProblemPlugin):
    problem_id   = "my-problem"
    title        = "My Problem"
    method_name  = "solve"          # method on user's Solution class
    difficulty   = "Easy"
    pattern      = "Array"
    description  = "Find the maximum element."

    def get_test_cases(self):
        return [
            TestCase(inputs={"nums": [1, 3, 2]}, expected=3, description="basic"),
            TestCase(inputs={"nums": [5]},       expected=5, description="single"),
            TestCase(inputs={"nums": []},        expected=None, description="empty",
                     is_hidden=True),
        ]

    def get_validator(self):
        return EqualityValidator()

# At module level, instantiate and register:
PLUGIN = MyProblem()
```

That's it. The registry auto-discovers `ProblemPlugin` subclasses on import.
Restart the server — `GET /api/problems` will list it, and
`POST /api/run-solution` with `problem_id="my-problem"` runs it.

### Tips
- **Custom validator**: subclass `Validator`, implement `validate(actual, expected) -> ValidationResult`. Return it from `get_validator()`.
- **Custom wrapper template**: override `get_wrapper_template()` to return a `WrapperTemplate(template_str=..., helpers_str=..., imports_str=...)`. Use `{solution_code}`, `{param_name}`, `{helpers}`, `{imports}` placeholders.
- **Pattern auto-routing**: setting `pattern = "Linked List"` / `"Tree"` / `"Graph"` / `"In-Place"` makes the engine pick the matching built-in wrapper template automatically.

---

## Adding a new wrapper template

1. Pick a pattern keyword (e.g. `"Heap"`).
2. Add a `HEAP_TEMPLATE` constant in `wrapper_generator.py`. Use placeholders:
   - `{imports}`, `{helpers}`, `{solution_code}` — auto-filled
   - `{param_assignments}` — already-indented `name = value` lines
   - `{param_names}`, `{before_captures}`, `{after_captures}`
3. Print `__RESULT__:` then `repr(result)` so the runner can parse it.
4. Wire it in `_select_template()` keyed off `plugin.pattern`.

**Indentation rule**: `{param_assignments}` lines must each carry their own
4-space indent; the template placeholder itself must NOT be pre-indented
(`def main():\n{param_assignments}` — not `def main():\n    {param_assignments}`).

**f-string rule**: marker prints must use plain strings, not f-strings:
`print("__RESULT__:")`, never `print(f"__RESULT__:")`. When interpolating a
value, use single braces: `print(repr(result))` or `f"{repr(result)}"`.

---

## Adding a new parameter type

1. Add the type to `type_hints.py` (`parse_type_hint` recognition).
2. Add a builder in `object_builder.py` (e.g. `build_heap(items)`).
3. Add helper code (e.g. `HEAP_HELPERS = "class Heap: ..."`) to inject into wrappers.
4. (Optional) Add a serializer + validator.

---

## Adding a new language engine (future)

The frontend is language-agnostic — it consumes standardized snapshots.
To add Java/C++/JS:

1. Implement the same `ExecutionResult` JSON contract in your new engine.
2. Each test must emit trace snapshots in the same schema as `tracer.py`
   (`Snapshot.to_dict()`): `{line, event, function, locals, globals, heap, ...}`.
3. Add a route like `POST /api/run-solution-java` or branch on a `language`
   field in the existing route.

No frontend changes needed — `adaptBackendTrace.js` handles the rest.

---

## Security

`security.sanitize_source()` performs an AST walk and rejects:

- **Imports**: `os`, `sys`, `subprocess`, `socket`, `http`, `urllib`, `ctypes`,
  `importlib`, `signal`, `multiprocessing`, `threading`, `shelve`, `pickle`,
  `pathlib`, …
- **Calls**: `eval`, `exec`, `compile`, `__import__`.
- **Dunder access**: `__globals__`, `__builtins__`, `__subclasses__`, …

Violations raise `SecurityViolationError` and the run aborts before any code
is executed. User solutions also run under a restricted globals dict.

---

## Error handling

`errors.classify_error(exc)` maps 15+ Python exception types to
`(error_type, human_message)`:

| Python | `error_type` |
|---|---|
| `SyntaxError` / `IndentationError` | `syntax_error` |
| `ImportError` / `ModuleNotFoundError` | `import_error` |
| `TypeError` | `type_error` |
| `IndexError` / `KeyError` | `index_error` / `key_error` |
| `AttributeError` | `attribute_error` |
| `RecursionError` | `recursion_error` |
| `NameError` / `ValueError` | `name_error` / `value_error` |
| `ZeroDivisionError` | `zero_division_error` |
| `AssertionError` | `assertion_error` |
| `MemoryError` | `memory_error` |
| `OverflowError` | `overflow_error` |
| `KeyboardInterrupt` | `interrupted` |
| `TimeoutError` (from tracer) | `timeout` |
| (other) | `runtime_error` |

Each `TestCaseResult` carries `exception`, `traceback`, and the classified
`error_type`, surfaced per-test in the frontend.

---

## Built-in problems (7)

| ID | Pattern | Method | Tests |
|---|---|---|---|
| `two-sum` | Hashing | `twoSum` | 6 |
| `binary-search` | Binary Search | `search` | 5 |
| `merge-sorted-array` | In-Place | `merge` | 4 |
| `reverse-linked-list` | Linked List | `reverseList` | 5 |
| `max-depth-binary-tree` | Tree | `maxDepth` | 5 |
| `valid-parentheses` | Stack | `isValid` | 7 |
| `number-of-islands` | Graph/Matrix | `numIslands` | 5 |

**Ambiguity**: when `method_name` matches multiple problems and no
`problem_id` is supplied, `run_solution()` returns early with
`ambiguous_problems` populated (no execution). The frontend then shows
`ProblemSelector` and re-submits with an explicit `problem_id`. We never
guess.

---

## Testing

Verified end-to-end (37/37 tests across all 7 problems) plus:

- Security blocks unsafe imports / calls / dunders.
- No-`Solution`-class detection (`error_type: no_solution`).
- `find_by_method()` returns all matches for ambiguity.
- Backward compatibility: `POST /api/run`, `/api/health`, `/api/config`
  unchanged and working.
