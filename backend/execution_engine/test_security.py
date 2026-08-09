"""
Security regression tests for the LeetCode execution engine.

Each test verifies an actual execution verdict — not just that an AST check
raises an exception. Tests run the full execute_isolated_python() path so
they cover both the AST pre-filter (security.py) and the runtime import guard
(SAFE_BUILTINS / _safe_import in tracer.py).

Run with:
    python -m unittest backend.execution_engine.test_security -v
"""

import unittest

from backend.execution_engine.security import sanitize_source, SecurityViolationError
from backend.execution_engine.runner import run_solution
from backend.models import ExecutionConfig
from backend.tracer import execute_isolated_python


# Shared tight config so tests finish quickly
TIGHT = ExecutionConfig(max_time_seconds=1.0, max_steps=200_000, max_recursion_depth=64)

# Two Sum wrapper — gives us a real plugin context for end-to-end tests
TWO_SUM = (
    "class Solution:\n"
    "    def twoSum(self, nums, target):\n"
    "        {body}\n"
)


def ts(body: str) -> str:
    """Build a two-sum solution with the given method body."""
    return TWO_SUM.format(body=body)


class ASTFilterTests(unittest.TestCase):
    """Fast, synchronous checks — just the AST scanner, no subprocess."""

    # --- Imports -----------------------------------------------------------

    def test_blocks_os_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import os")

    def test_blocks_sys_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import sys")

    def test_blocks_subprocess_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import subprocess")

    def test_blocks_socket_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import socket")

    def test_blocks_shutil_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import shutil")

    def test_blocks_pathlib_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import pathlib")

    def test_blocks_ctypes_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import ctypes")

    def test_blocks_multiprocessing_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import multiprocessing")

    def test_blocks_threading_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import threading")

    def test_blocks_importlib_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import importlib")

    def test_blocks_pickle_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import pickle")

    def test_blocks_signal_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import signal")

    def test_blocks_resource_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("import resource")

    # --- Forbidden calls ---------------------------------------------------

    def test_blocks_eval(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("eval('1+1')")

    def test_blocks_exec(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("exec('x=1')")

    def test_blocks_compile(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("compile('x', '<s>', 'exec')")

    def test_blocks_open(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("open('file.txt')")

    def test_blocks_globals(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("globals()")

    def test_blocks_locals(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("locals()")

    def test_blocks_vars(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("vars()")

    def test_blocks_dunder_import(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("__import__('os')")

    def test_blocks_breakpoint(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("breakpoint()")

    # --- Dangerous attribute access ----------------------------------------

    def test_blocks_subclasses_attribute(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("object.__subclasses__()")

    def test_blocks_mro_attribute(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("int.mro()")

    def test_blocks_builtins_name(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("x = __builtins__")

    def test_blocks_code_attribute(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("f.__code__")

    def test_blocks_globals_attribute(self):
        with self.assertRaises(SecurityViolationError):
            sanitize_source("f.__globals__")

    # --- Allowed imports (must NOT raise) ----------------------------------

    def test_allows_typing(self):
        sanitize_source("from typing import List, Optional")

    def test_allows_collections(self):
        sanitize_source("from collections import defaultdict, deque, Counter")

    def test_allows_heapq(self):
        sanitize_source("import heapq")

    def test_allows_math(self):
        sanitize_source("import math")

    def test_allows_bisect(self):
        sanitize_source("import bisect")

    def test_allows_functools(self):
        sanitize_source("import functools")

    def test_allows_itertools(self):
        sanitize_source("import itertools")

    def test_allows_re(self):
        sanitize_source("import re")

    def test_allows_copy(self):
        sanitize_source("import copy")

    def test_allows_random(self):
        sanitize_source("import random")


class RuntimeIsolationTests(unittest.TestCase):
    """End-to-end tests via execute_isolated_python() — full worker path."""

    def _run(self, code: str, cfg: ExecutionConfig = None):
        return execute_isolated_python(code, "", cfg or TIGHT)

    # --- Dangerous imports blocked at runtime ------------------------------

    def test_runtime_blocks_os(self):
        _, err, _, etype = self._run("import os; os.system('echo pwned')")
        self.assertIsNotNone(err)
        self.assertIn("allowed", err.lower())

    def test_runtime_blocks_subprocess(self):
        _, err, _, _ = self._run("import subprocess; subprocess.run(['echo','x'])")
        self.assertIsNotNone(err)

    def test_runtime_blocks_socket(self):
        _, err, _, _ = self._run("import socket; socket.create_connection(('8.8.8.8',53))")
        self.assertIsNotNone(err)

    def test_runtime_blocks_ctypes(self):
        _, err, _, _ = self._run("import ctypes")
        self.assertIsNotNone(err)

    def test_runtime_blocks_importlib(self):
        _, err, _, _ = self._run("import importlib; importlib.import_module('os')")
        self.assertIsNotNone(err)

    # --- File-system access -----------------------------------------------

    def test_runtime_no_open_write(self):
        # open() is in SAFE_BUILTINS? No — it was removed. Should fail.
        _, err, _, _ = self._run("open('/tmp/test.txt', 'w').write('x')")
        self.assertIsNotNone(err, "open() should not be available at runtime")

    def test_runtime_no_open_read(self):
        _, err, _, _ = self._run("open('/etc/passwd').read()")
        self.assertIsNotNone(err, "open() for reading should not be available")

    # --- Dynamic execution ------------------------------------------------

    def test_runtime_no_eval(self):
        # eval() is not in SAFE_BUILTINS
        _, err, _, _ = self._run("eval('1+1')")
        self.assertIsNotNone(err)

    def test_runtime_no_exec(self):
        _, err, _, _ = self._run("exec('x=1')")
        self.assertIsNotNone(err)

    def test_runtime_no_compile(self):
        _, err, _, _ = self._run("compile('1','<s>','exec')")
        self.assertIsNotNone(err)

    # --- Environment access -----------------------------------------------

    def test_runtime_no_env_access_via_os(self):
        _, err, _, _ = self._run("import os; os.environ.get('SECRET')")
        self.assertIsNotNone(err)

    # --- Excessive output -------------------------------------------------

    def test_output_limit_enforced(self):
        cfg = ExecutionConfig(max_output_chars=100, max_steps=200_000)
        _, err, _, etype = self._run("print('x'*1000)", cfg)
        self.assertIsNotNone(err)
        self.assertEqual(etype, "output_limit")

    # --- Recursion limit --------------------------------------------------

    def test_recursion_limit_enforced(self):
        cfg = ExecutionConfig(max_recursion_depth=20, max_steps=200_000)
        _, err, _, etype = self._run(
            "def f(): return f()\nf()", cfg
        )
        self.assertIsNotNone(err)
        self.assertIn(etype, {"recursion_limit", "runtime_error"})

    # --- Step limit -------------------------------------------------------

    def test_step_limit_enforced(self):
        cfg = ExecutionConfig(max_steps=500, max_time_seconds=10.0)
        _, err, _, etype = self._run("x=0\nwhile True:\n x+=1", cfg)
        self.assertIsNotNone(err)
        self.assertIn(etype, {"step_limit", "time_limit"})

    # --- Wall-clock timeout -----------------------------------------------

    def test_wall_clock_timeout(self):
        cfg = ExecutionConfig(max_time_seconds=0.8, max_steps=200_000)
        _, err, _, etype = self._run("x=0\nwhile True:\n x+=1", cfg)
        self.assertIsNotNone(err)
        self.assertIn(etype, {"time_limit", "step_limit"})


class FullJudgeSecurityTests(unittest.TestCase):
    """Security tests via the full run_solution() judge path."""

    def _judge(self, body: str, cfg: ExecutionConfig = None):
        code = ts(body)
        return run_solution(code, problem_id="two-sum", config=cfg or TIGHT)

    # --- AST filter catches before execution --------------------------------

    def test_verdict_security_violation_for_open(self):
        result = self._judge("open('evil.txt')\n        return []")
        self.assertEqual(result.to_dict()["status"], "SECURITY_VIOLATION")

    def test_verdict_security_violation_for_os_import(self):
        code = "import os\nclass Solution:\n    def twoSum(self, nums, target):\n        return []"
        result = run_solution(code, problem_id="two-sum")
        self.assertEqual(result.to_dict()["status"], "SECURITY_VIOLATION")

    def test_verdict_security_violation_for_eval(self):
        result = self._judge("eval('1')\n        return []")
        self.assertEqual(result.to_dict()["status"], "SECURITY_VIOLATION")

    def test_verdict_security_violation_for_subprocess(self):
        code = "import subprocess\nclass Solution:\n    def twoSum(self, nums, target):\n        return []"
        result = run_solution(code, problem_id="two-sum")
        self.assertEqual(result.to_dict()["status"], "SECURITY_VIOLATION")

    # --- Infinite loop killed as TLE ----------------------------------------

    def test_infinite_loop_is_tle(self):
        cfg = ExecutionConfig(max_time_seconds=0.8, max_steps=200_000)
        result = self._judge("while True: pass", cfg)
        status = result.to_dict()["status"]
        self.assertIn(status, {"TIME_LIMIT_EXCEEDED", "WRONG_ANSWER"})
        # Must not be ACCEPTED
        self.assertNotEqual(status, "ACCEPTED")

    def test_tight_step_loop_is_tle(self):
        cfg = ExecutionConfig(max_steps=1000, max_time_seconds=10.0)
        result = self._judge("x=0\nwhile True:\n            x+=1", cfg)
        status = result.to_dict()["status"]
        self.assertIn(status, {"TIME_LIMIT_EXCEEDED", "RUNTIME_ERROR"})

    # --- Correct solution still passes --------------------------------------

    def test_correct_solution_accepted(self):
        code = (
            "class Solution:\n"
            "    def twoSum(self, nums, target):\n"
            "        seen = {}\n"
            "        for i, v in enumerate(nums):\n"
            "            if target-v in seen:\n"
            "                return [seen[target-v], i]\n"
            "            seen[v] = i\n"
            "        return []\n"
        )
        result = run_solution(code, problem_id="two-sum")
        self.assertEqual(result.to_dict()["status"], "ACCEPTED")

    # --- Wrong answer not accepted ------------------------------------------

    def test_wrong_answer_rejected(self):
        result = self._judge("return [0, 0]")
        self.assertEqual(result.to_dict()["status"], "WRONG_ANSWER")

    # --- Syntax error -------------------------------------------------------

    def test_syntax_error_reported(self):
        code = "class Solution:\n    def twoSum(self, nums, target):\n        return ["
        result = run_solution(code, problem_id="two-sum")
        self.assertIn(result.to_dict()["status"], {"COMPILATION_ERROR", "RUNTIME_ERROR"})

    # --- Hidden tests redacted -----------------------------------------------

    def test_hidden_test_fields_absent(self):
        code = "class Solution:\n    def twoSum(self, nums, target):\n        return []"
        payload = run_solution(code, problem_id="two-sum").to_dict()
        for t in payload["test_results"]:
            if t["hidden"]:
                self.assertNotIn("input_repr", t)
                self.assertNotIn("expected", t)
                self.assertNotIn("actual", t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
