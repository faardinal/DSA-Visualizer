"""
Binary Search problem plugin.
Pattern: Binary Search
Difficulty: Easy

Note: method_name is "search" — this demonstrates ambiguity since other
problems (Search Rotated Array, First Bad Version) also use "search".
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
)


class BinarySearchPlugin(ProblemPlugin):
    problem_id = "binary-search"
    title = "Binary Search"
    method_name = "search"
    difficulty = "Easy"
    pattern = "Binary Search"
    description = (
        "Given an array of integers nums sorted in ascending order and "
        "an integer target, return the index of target. If not found, return -1."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={"nums": [-1, 0, 3, 5, 9, 12], "target": 9},
                expected=4,
                description="Example 1: found",
                is_hidden=False,
            ),
            TestCase(
                inputs={"nums": [-1, 0, 3, 5, 9, 12], "target": 2},
                expected=-1,
                description="Example 2: not found",
                is_hidden=False,
            ),
            TestCase(
                inputs={"nums": [5], "target": 5},
                expected=0,
                description="Single element, found",
                is_hidden=False,
            ),
            TestCase(
                inputs={"nums": [2, 5], "target": 5},
                expected=1,
                description="Hidden: two elements, found",
                is_hidden=True,
            ),
            TestCase(
                inputs={"nums": list(range(10000)), "target": 9999},
                expected=9999,
                description="Hidden: large array, last element",
                is_hidden=True,
            ),
        ]

    def get_validator(self):
        return EqualityValidator()


class EqualityValidator(Validator):
    """Simple equality validator."""

    def validate(self, actual, expected):
        actual_repr = repr(actual)
        expected_repr = repr(expected)
        passed = actual == expected
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)
