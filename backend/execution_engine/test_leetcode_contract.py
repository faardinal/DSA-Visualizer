"""Regression tests for the LeetCode submission contract."""

import unittest

from backend.execution_engine import get_registry, run_solution
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


class LeetCodeContractTests(unittest.TestCase):
    def test_registered_plugins_have_oracle_backed_hidden_cases(self):
        for problem_id in get_registry().get_all_problem_ids():
            plugin = get_registry().get(problem_id)
            definition = plugin.get_definition()
            self.assertIsNotNone(definition.oracle, problem_id)
            self.assertIsNotNone(definition.generator, problem_id)
            self.assertGreater(definition.hidden_test_count, 0, problem_id)

    def test_standard_leetcode_typing_needs_no_user_import(self):
        result = run_solution(TWO_SUM_SOLUTION, problem_id="two-sum", seed=17)
        self.assertTrue(result.passed)
        self.assertEqual(result.to_dict()["status"], "ACCEPTED")

    def test_replay_uses_the_same_persisted_test_inputs(self):
        first = run_solution(TWO_SUM_SOLUTION, problem_id="two-sum", seed=19)
        replay = run_solution(
            TWO_SUM_SOLUTION,
            problem_id="two-sum",
            session_id=first.session_id,
            replay_test_idx=4,
        )
        self.assertEqual(first.seed, replay.seed)
        self.assertEqual(first.test_results[4].expected, replay.test_results[4].expected)
        self.assertGreater(len(replay.trace), 0)

    def test_hidden_details_are_redacted_from_api_payload(self):
        result = run_solution(
            "class Solution:\n    def twoSum(self, nums, target):\n        return []",
            problem_id="two-sum",
            seed=23,
        ).to_dict()
        hidden = next(test for test in result["test_results"] if test["hidden"])
        self.assertNotIn("input_repr", hidden)
        self.assertNotIn("expected", hidden)
        self.assertNotIn("actual", hidden)

    def test_file_access_is_rejected_before_execution(self):
        result = run_solution(
            "class Solution:\n    def twoSum(self, nums, target):\n        open('blocked.txt', 'w')\n        return []",
            problem_id="two-sum",
        )
        self.assertEqual(result.to_dict()["status"], "SECURITY_VIOLATION")
        self.assertIn("open", result.error)

    def test_obvious_reflection_and_network_paths_are_rejected(self):
        for source in ("globals()", "type(1).mro()", "import socket"):
            with self.assertRaises(Exception):
                sanitize_source(source)

    def test_infinite_loop_is_killed_by_the_submission_deadline(self):
        result = run_solution(
            "class Solution:\n    def twoSum(self, nums, target):\n        while True:\n            pass",
            problem_id="two-sum",
            config=ExecutionConfig(max_time_seconds=0.5, max_steps=100_000),
        )
        self.assertEqual(result.to_dict()["status"], "TIME_LIMIT_EXCEEDED")

    def test_excessive_output_is_limited(self):
        result = run_solution(
            "class Solution:\n    def twoSum(self, nums, target):\n        print('x' * 500)\n        return []",
            problem_id="two-sum",
            config=ExecutionConfig(max_output_chars=64),
        )
        self.assertEqual(result.to_dict()["status"], "RUNTIME_ERROR")
        self.assertEqual(result.test_results[0].error_type, "output_limit")

    def test_recursion_limit_is_reported(self):
        result = run_solution(
            "class Solution:\n    def twoSum(self, nums, target):\n        return self.twoSum(nums, target)",
            problem_id="two-sum",
            config=ExecutionConfig(max_recursion_depth=32),
        )
        self.assertEqual(result.to_dict()["status"], "RUNTIME_ERROR")
        self.assertIn(result.test_results[0].error_type, {"recursion_limit", "runtime_error"})


if __name__ == "__main__":
    unittest.main()
