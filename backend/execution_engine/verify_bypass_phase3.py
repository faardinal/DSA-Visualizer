"""
Phase 3 security BYPASS-ATTEMPT verification.

The AST filter is the primary gate. The runtime (`_safe_import` + scrubbed
builtins) must be defense-in-depth for anything the AST does NOT statically
catch. This script tries realistic obfuscation/bypass techniques and confirms
NONE of them let forbidden code run to completion.

If any of these 'pass' (escape), that is a real Phase 3 security hole.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.execution_engine import run_solution
from backend.execution_engine.security import sanitize_source
from backend.models import ExecutionConfig

STRICT = ExecutionConfig(max_time_seconds=1.0, max_steps=50_000,
                         max_recursion_depth=300, max_output_chars=4_000)


def _run(source, problem_id="two-sum", config=STRICT):
    return run_solution(source, problem_id=problem_id, config=config).to_dict()


def _contained(result):
    return result.get("status") in {
        "SECURITY_VIOLATION", "TIME_LIMIT_EXCEEDED", "RUNTIME_ERROR",
        "MEMORY_LIMIT_EXCEEDED", "COMPILATION_ERROR", "METHOD_ERROR",
        "PROBLEM_NOT_FOUND",
    }


RESULTS = []


def check(name, condition, detail=""):
    RESULTS.append((name, condition, detail))
    tag = "PASS" if condition else "FAIL"
    print(f"  {tag}  {name}" + (f"  ({detail})" if detail else ""))


# Wrap every payload inside a Solution.twoSum so it goes through run_solution.
def wrap(body):
    return "class Solution:\n    def twoSum(self, nums, target):\n" + \
           "\n".join("        " + line for line in body.splitlines()) + "\n        return []\n"


print("=== Bypass attempts (defense-in-depth) ===")

# 1. __import__ is in FORBIDDEN_CALLS -> AST should catch the direct call
try:
    sanitize_source("x = __import__('os')")
    check("__import__ direct call blocked by AST", False)
except Exception:
    check("__import__ direct call blocked by AST", True)

# 2. getattr(builtins, '__import__') — getattr is forbidden, dunder blocked
try:
    sanitize_source("getattr(__builtins__, '__import__')('os')")
    check("getattr+__import__ blocked by AST", False)
except Exception:
    check("getattr+__import__ blocked by AST", True)

# 3. Try to reach builtins through a function object — __globals__/__builtins__ dunders blocked
try:
    sanitize_source("def f():\n    pass\nf.__globals__['__builtins__']['open']('x')")
    check("func.__globals__ blocked by AST", False)
except Exception:
    check("func.__globals__ blocked by AST", True)

# 4. Builtins via dict literal trickery — still references __builtins__
try:
    sanitize_source("x = {1:2}\nx.__class__")
    check("dict.__class__ dunder blocked by AST", False)
except Exception:
    check("dict.__class__ dunder blocked by AST", True)

# 5. exec via a variable alias — exec is a Name call, AST blocks the call
r = _run(wrap("e = eval\nreturn e('1+1')"))
check("eval aliasing blocked end-to-end", _contained(r), r.get("status"))

# 6. Runtime: an import the AST might not have on its forbidden list but that
#    is still dangerous (e.g. 'platform' reads env, 'inspect' reads frames).
#    These are NOT in FORBIDDEN_MODULES, so AST lets them through — the runtime
#    _safe_import must reject them because they're not in ALLOWED_RUNTIME_MODULES.
r = _run(wrap("import platform\nreturn [platform.platform()]"))
check("non-allowlisted import (platform) rejected at runtime", _contained(r), r.get("status"))

r = _run(wrap("import inspect\nreturn []"))
check("non-allowlisted import (inspect) rejected at runtime", _contained(r), r.get("status"))

r = _run(wrap("import builtins\nreturn []"))
check("import builtins rejected at runtime", _contained(r), r.get("status"))

# 7. Compile/exec builtins are NOT in SAFE_BUILTINS, so even if AST missed them,
#    runtime NameError. Confirm eval/exec are absent from the runtime namespace.
r = _run(wrap("return eval('1+1')"))
check("eval not available at runtime", _contained(r), r.get("status"))

r = _run(wrap("exec('x=2')"))
check("exec not available at runtime", _contained(r), r.get("status"))

# 8. open is NOT in SAFE_BUILTINS — runtime would NameError even without AST.
#    (AST catches it first as SECURITY_VIOLATION, but verify runtime too by
#     reaching open through a non-blocked path is impossible.)
r = _run(wrap("f = open('x')"))
check("open() contained end-to-end", _contained(r), r.get("status"))

# 9. __builtins__ access in the worker — confirm the scrubbed namespace wins.
r = _run(wrap("return __builtins__"))
check("__builtins__ access contained", _contained(r), r.get("status"))

# 10. globals()/locals() are in FORBIDDEN_CALLS and not in SAFE_BUILTINS.
try:
    sanitize_source("return globals()")
    check("globals() blocked by AST", False)
except Exception:
    check("globals() blocked by AST", True)

print("\n=== SUMMARY ===")
passed = sum(1 for _, ok, _ in RESULTS if ok)
failed = sum(1 for _, ok, _ in RESULTS if not ok)
for name, ok, detail in RESULTS:
    if not ok:
        print(f"  FAILED: {name}  ({detail})")
print(f"\n{passed} passed, {failed} failed out of {len(RESULTS)} checks")
if failed:
    raise SystemExit(1)
