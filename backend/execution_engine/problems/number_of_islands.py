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
    leetcode_number = 200
    slug = "number-of-islands"
    title = "Number of Islands"
    method_name = "numIslands"
    difficulty = "Medium"
    pattern = "Graph"
    topics = ["Array", "Depth-First Search", "Breadth-First Search", "Matrix"]
    parameters = ["grid: List[List[str]]"]
    return_type = "int"
    mutation_strategy = "grid"
    hidden_test_count = 2
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

    @staticmethod
    def oracle(inputs):
        grid = [row[:] for row in inputs["grid"]]
        islands = 0
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] != "1":
                    continue
                islands += 1
                stack = [(row, col)]
                grid[row][col] = "0"
                while stack:
                    current_row, current_col = stack.pop()
                    for next_row, next_col in ((current_row - 1, current_col), (current_row + 1, current_col), (current_row, current_col - 1), (current_row, current_col + 1)):
                        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[next_row]) and grid[next_row][next_col] == "1":
                            grid[next_row][next_col] = "0"
                            stack.append((next_row, next_col))
        return islands

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            rows, cols = rng.randint(0, 10), rng.randint(0, 10)
            tests.append({"grid": [[rng.choice(["0", "1"]) for _ in range(cols)] for _ in range(rows)]})
        return tests


class EqualityValidator(Validator):
    """Simple equality validator."""

    def validate(self, actual, expected):
        actual_repr = repr(actual)
        expected_repr = repr(expected)
        passed = actual == expected
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)
