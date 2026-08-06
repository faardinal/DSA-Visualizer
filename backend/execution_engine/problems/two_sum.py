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
    title = "Two Sum"
    method_name = "twoSum"
    difficulty = "Easy"
    pattern = "Hashing"
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

    def validate(self, actual, expected):
        actual_repr = repr(actual)
        expected_repr = repr(expected)

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
