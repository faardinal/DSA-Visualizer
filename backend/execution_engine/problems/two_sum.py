"""
Two Sum problem plugin.
Pattern: Hashing
Difficulty: Easy

Given an array of integers and a target, return indices of the two numbers
that add up to the target.
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
)


class TwoSumPlugin(ProblemPlugin):
    problem_id = "two-sum"
    leetcode_number = 1
    slug = "two-sum"
    title = "Two Sum"
    method_name = "twoSum"
    difficulty = "Easy"
    pattern = "Hashing"
    topics = ["Array", "Hash Table"]
    parameters = ["nums: List[int]", "target: int"]
    return_type = "List[int]"
    constraints = "2 <= nums.length <= 10^4; exactly one answer exists."
    hidden_test_count = 3
    description = (
        "Given an array of integers nums and an integer target, "
        "return indices of the two numbers such that they add up to target."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={"nums": [2, 7, 11, 15], "target": 9},
                expected=[0, 1],
                description="Example 1",
                is_hidden=False,
            ),
            TestCase(
                inputs={"nums": [3, 2, 4], "target": 6},
                expected=[1, 2],
                description="Example 2",
                is_hidden=False,
            ),
            TestCase(
                inputs={"nums": [3, 3], "target": 6},
                expected=[0, 1],
                description="Example 3: duplicates",
                is_hidden=False,
            ),
            TestCase(
                inputs={"nums": [1, 5, 3, 7, 2, 8], "target": 10},
                expected=[2, 3],
                description="Hidden: multiple pairs",
                is_hidden=True,
            ),
            TestCase(
                inputs={"nums": [-1, -2, -3, -4, -5], "target": -8},
                expected=[2, 4],
                description="Hidden: negative numbers",
                is_hidden=True,
            ),
            TestCase(
                inputs={"nums": [0, 4, 3, 0], "target": 0},
                expected=[0, 3],
                description="Hidden: zeros",
                is_hidden=True,
            ),
        ]

    def get_validator(self):
        return TwoSumValidator()

    @staticmethod
    def oracle(inputs):
        nums, target = inputs["nums"], inputs["target"]
        for left in range(len(nums)):
            for right in range(left + 1, len(nums)):
                if nums[left] + nums[right] == target:
                    return [left, right]
        return []

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for index in range(count):
            size = rng.randint(2, 30)
            nums = [rng.randint(-100, 100) for _ in range(size)]
            left, right = rng.sample(range(size), 2)
            tests.append({"nums": nums, "target": nums[left] + nums[right]})
        return tests


class TwoSumValidator(Validator):
    """
    Validator for Two Sum.

    LeetCode accepts any valid index pair whose values sum to target, but
    verifying that requires the original (nums, target) inputs which the
    validator interface doesn't receive. We therefore accept the expected
    answer OR its reverse — both are correct for the curated test cases,
    and any other pair is rejected. This is intentionally strict: an
    arbitrary [0, 1] returned by a stub solution must NOT pass.
    """

    def validate(self, actual, expected, inputs=None):
        actual_repr = repr(actual)
        expected_repr = repr(expected)

        if inputs and isinstance(actual, (list, tuple)) and len(actual) == 2:
            nums, target = inputs["nums"], inputs["target"]
            left, right = actual
            if (isinstance(left, int) and isinstance(right, int)
                    and 0 <= left < len(nums) and 0 <= right < len(nums)
                    and left != right and nums[left] + nums[right] == target):
                return ValidationResult(True, expected_repr, actual_repr, "Valid index pair")

        # Exact match
        if actual == expected:
            return ValidationResult(True, expected_repr, actual_repr)

        # Reversed order of the same expected pair is also valid
        if (isinstance(actual, (list, tuple))
                and len(actual) == 2
                and list(actual) == [expected[1], expected[0]]):
            return ValidationResult(True, expected_repr, actual_repr,
                                     "Valid answer (reversed order)")

        return ValidationResult(False, expected_repr, actual_repr,
                                 f"Expected {expected_repr}, got {actual_repr}")
