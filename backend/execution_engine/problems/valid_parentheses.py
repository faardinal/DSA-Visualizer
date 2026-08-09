"""
Valid Parentheses problem plugin.
Pattern: Stack
Difficulty: Easy
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
)


class ValidParenthesesPlugin(ProblemPlugin):
    problem_id = "valid-parentheses"
    leetcode_number = 20
    slug = "valid-parentheses"
    title = "Valid Parentheses"
    method_name = "isValid"
    difficulty = "Easy"
    pattern = "Stack"
    topics = ["String", "Stack"]
    parameters = ["s: str"]
    return_type = "bool"
    hidden_test_count = 3
    description = (
        "Given a string s containing just the characters '(', ')', '{', '}', "
        "'[' and ']', determine if the input string is valid."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={"s": "()"},
                expected=True,
                description="Example 1",
                is_hidden=False,
            ),
            TestCase(
                inputs={"s": "()[]{}"},
                expected=True,
                description="Example 2",
                is_hidden=False,
            ),
            TestCase(
                inputs={"s": "(]"},
                expected=False,
                description="Example 3",
                is_hidden=False,
            ),
            TestCase(
                inputs={"s": ""},
                expected=True,
                description="Empty string",
                is_hidden=False,
            ),
            TestCase(
                inputs={"s": "([{}])"},
                expected=True,
                description="Hidden: nested",
                is_hidden=True,
            ),
            TestCase(
                inputs={"s": "((("},
                expected=False,
                description="Hidden: only opens",
                is_hidden=True,
            ),
            TestCase(
                inputs={"s": "{[()]}{[({})]}"},
                expected=True,
                description="Hidden: complex valid",
                is_hidden=True,
            ),
        ]

    def get_validator(self):
        return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for char in inputs["s"]:
            if char in pairs:
                if not stack or stack.pop() != pairs[char]:
                    return False
            else:
                stack.append(char)
        return not stack

    @staticmethod
    def generate_hidden_inputs(rng, count):
        alphabet = "()[]{}"
        return [{"s": "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 50)))} for _ in range(count)]


class EqualityValidator(Validator):
    """Simple equality validator."""

    def validate(self, actual, expected):
        actual_repr = repr(actual)
        expected_repr = repr(expected)
        passed = actual == expected
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)
