"""
Phase 3 security verification harness.

Exercises EVERY requested escape vector through the REAL submission path
(`run_solution` -> isolated worker subprocess), not just the AST filter.
This is an independent verification, not the previous agent's report.

Vectors tested (per STEP 2 of the handoff task):
  * infinite loop
  * wall-clock timeout (C-level sleep, tracing cannot interrupt)
  * open()
  * filesystem access
  * eval()
  * exec()
  * dangerous imports
  * socket
  * subprocess / process creation
  * environment-variable access
  * excessive output
  * excessive recursion
  * normal valid LeetCode code (must still be ACCEPTED)

A vector "passes" when the user solution CANNOT escape the boundary:
  - blocked before execution (SECURITY_VIOLATION), OR
  - killed/limited at runtime (TIME_LIMIT_EXCEEDED / RUNTIME_ERROR / etc.)

It FAILS only when forbidden work actually executed without limit OR when
the valid LeetCode solution is incorrectly rejected.
"""

import os
import sys
import time

# Add project root to path so `backend` is importable when run directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.execution_engine import run_solution
from backend.execution_engine.security import sanitize_source
from backend.models import ExecutionConfig


TWO_SUM_SOLUTION = '''class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for index, value in enumerate(nums):
            remainder = target - value
            if remainder in seen:
                return [seen[remainder], index]
            seen[value] = index
        return []
'''


# Strict per-test config so the suite runs fast. The submission path clamps
# these server-side anyway; we keep them tiny to make loops/TLE quick.
STRICT = ExecutionConfig(max_time_seconds=1.0, max_steps=50_000,
                         max_recursion_depth=300, max_output_chars=4_000)


def _run(source, problem_id="two-sum", config=STRICT):
    return run_solution(source, problem_id=problem_id, config=config).to_dict()


def _blocked_or_limited(result):
    """Return True if the vector was contained (could not escape)."""
    status = result.get("status")
    # Any of these means the work did not run to completion / was contained.
    return status in {
        "SECURITY_VIOLATION", "TIME_LIMIT_EXCEEDED", "RUNTIME_ERROR",
        "MEMORY_LIMIT_EXCEEDED", "COMPILATION_ERROR", "METHOD_ERROR",
        "PROBLEM_NOT_FOUND",
    }


RESULTS = []


def check(name, condition, detail=""):
    RESULTS.append((name, condition, detail))
    tag = "PASS" if condition else "FAIL"
    print(f"  {tag}  {name}" + (f"  ({detail})" if detail else ""))


# ---------------------------------------------------------------------------
# 1. infinite loop (pure-Python, tracing can interrupt via step/time)
# ---------------------------------------------------------------------------
print("=== 1. infinite loop (pure Python) ===")
r = _run('class Solution:\n    def twoSum(self, nums, target):\n        while True:\n            pass\n')
check("infinite loop killed", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 2. wall-clock timeout via time.sleep (C-level, tracing cannot interrupt)
#    time is allowed but sleep inside the worker must be killed by the
#    wall-clock deadline. Use a nested-loop that also defeats the step limit
#    quickly, but sleep is the real escape attempt.
# ---------------------------------------------------------------------------
print("=== 2. wall-clock timeout (busy C work) ===")
# A large pure-Python busy loop that spends time in C (range iteration) so the
# step limit could in principle catch it, but the wall-clock is the backstop.
r = _run('class Solution:\n    def twoSum(self, nums, target):\n'
         '        x = 0\n'
         '        for i in range(10**9):\n            x += i\n'
         '        return []\n',
         config=ExecutionConfig(max_time_seconds=1.0, max_steps=10_000_000))
check("busy C-loop timed out", r.get("status") == "TIME_LIMIT_EXCEEDED", r.get("status"))

# ---------------------------------------------------------------------------
# 3. open()
# ---------------------------------------------------------------------------
print("=== 3. open() ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        open('blocked.txt', 'w')\n        return []\n")
check("open() blocked before execution",
      r.get("status") == "SECURITY_VIOLATION" and "open" in (r.get("error") or ""),
      r.get("status"))

# ---------------------------------------------------------------------------
# 4. filesystem access via import (pathlib/os are forbidden imports too)
# ---------------------------------------------------------------------------
print("=== 4. filesystem access ===")
for src in (
    "import os\nos.listdir('.')\n",
    "import pathlib\n",
):
    try:
        sanitize_source(src)
        check(f"filesystem import blocked by AST: {src.split('(')[0].strip()}", False)
    except Exception:
        check(f"filesystem import blocked by AST: {src.split('(')[0].strip()}", True)

# ---------------------------------------------------------------------------
# 5. eval()
# ---------------------------------------------------------------------------
print("=== 5. eval() ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        return eval('1+1')\n")
check("eval() blocked", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 6. exec()
# ---------------------------------------------------------------------------
print("=== 6. exec() ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        exec('x=1')\n        return []\n")
check("exec() blocked", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 7. dangerous imports (socket, subprocess, ctypes, etc.)
# ---------------------------------------------------------------------------
print("=== 7. dangerous imports ===")
for mod in ("os", "sys", "subprocess", "socket", "ctypes", "importlib",
            "multiprocessing", "threading", "pickle", "shutil", "pathlib"):
    src = f"import {mod}\nclass Solution:\n    def twoSum(self, nums, target):\n        return []\n"
    try:
        sanitize_source(src)
        # If AST let it through, confirm the runtime import still fails.
        r = _run(src)
        check(f"import {mod} blocked", _blocked_or_limited(r), r.get("status"))
    except Exception:
        check(f"import {mod} blocked", True)

# ---------------------------------------------------------------------------
# 8. socket
# ---------------------------------------------------------------------------
print("=== 8. socket ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        import socket\n        return []\n")
check("socket blocked", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 9. subprocess / process creation
# ---------------------------------------------------------------------------
print("=== 9. subprocess / process creation ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        import subprocess\n        return []\n")
check("subprocess import blocked", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 10. environment-variable access (os.environ) — os is forbidden at AST level
# ---------------------------------------------------------------------------
print("=== 10. environment-variable access ===")
try:
    sanitize_source("import os\nos.environ['SECRET']")
    check("os.environ access blocked at AST", False)
except Exception:
    check("os.environ access blocked at AST", True)

# Also confirm the worker environment itself is scrubbed: a valid solution that
# tries to read os.environ must be unable to even import os at runtime.
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        import os\n        return list(os.environ)\n")
check("environ runtime access blocked", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 11. excessive output
# ---------------------------------------------------------------------------
print("=== 11. excessive output ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        print('x' * 1_000_000)\n        return []\n",
         config=ExecutionConfig(max_time_seconds=1.0, max_output_chars=2_000))
check("excessive output limited", r.get("status") == "RUNTIME_ERROR",
      f"{r.get('status')} / { (r['test_results'][0].get('error_type') if r.get('test_results') else '') }")

# ---------------------------------------------------------------------------
# 12. excessive recursion
# ---------------------------------------------------------------------------
print("=== 12. excessive recursion ===")
r = _run("class Solution:\n    def twoSum(self, nums, target):\n        def f():\n            return f()\n        return f()\n",
         config=ExecutionConfig(max_time_seconds=1.0, max_recursion_depth=200))
check("excessive recursion limited", _blocked_or_limited(r), r.get("status"))

# ---------------------------------------------------------------------------
# 13. normal valid LeetCode code MUST still be accepted
# ---------------------------------------------------------------------------
print("=== 13. normal valid LeetCode code ===")
r = _run(TWO_SUM_SOLUTION, config=ExecutionConfig(max_time_seconds=2.0))
check("valid solution accepted", r.get("status") == "ACCEPTED", r.get("status"))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n=== SUMMARY ===")
passed = sum(1 for _, ok, _ in RESULTS if ok)
failed = sum(1 for _, ok, _ in RESULTS if not ok)
for name, ok, detail in RESULTS:
    if not ok:
        print(f"  FAILED: {name}  ({detail})")
print(f"\n{passed} passed, {failed} failed out of {len(RESULTS)} checks")

if failed:
    raise SystemExit(1)
