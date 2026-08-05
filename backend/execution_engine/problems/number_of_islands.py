"""
Number of Islands problem plugin.
Pattern: Graph / DFS / Matrix
Difficulty: Medium
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
)


class NumberOfIslandsPlugin(ProblemPlugin):
    problem_id = "number-of-islands"
    title = "Number of Islands"
    method_name = "numIslands"
    difficulty = "Medium"
    pattern = "Graph"
    description = (
        "Given an m x n 2D binary grid which represents a map of '1's (land) "
        "and '0's (water), return the number of islands."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={
                    "grid": [
                        ["1", "1", "1", "1", "0"],
                        ["1", "1", "0", "1", "0"],
                        ["1", "1", "0", "0", "0"],
                        ["0", "0", "0", "0", "0"],
                    ]
                },
                expected=1,
                description="Example 1",
                is_hidden=False,
            ),
            TestCase(
                inputs={
                    "grid": [
                        ["1", "1", "0", "0", "0"],
                        ["1", "1", "0", "0", "0"],
                        ["0", "0", "1", "0", "0"],
                        ["0", "0", "0", "1", "1"],
                    ]
                },
                expected=3,
                description="Example 2",
                is_hidden=False,
            ),
            TestCase(
                inputs={"grid": [["0"]]},
                expected=0,
                description="Single cell, water",
                is_hidden=False,
            ),
            TestCase(
                inputs={"grid": [["1"]]},
                expected=1,
                description="Hidden: single cell, land",
                is_hidden=True,
            ),
            TestCase(
                inputs={"grid": []},
                expected=0,
                description="Hidden: empty grid",
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
