"""
Plugin base protocol for LeetCode-style problem definitions.

Each problem is a self-contained plugin file that implements the
ProblemPlugin ABC. The plugin registry discovers and manages these plugins.

To add a new problem:
1. Create a new .py file in the problems/ directory
2. Define a class extending ProblemPlugin
3. Implement the required abstract methods
4. The registry will auto-discover it on startup
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TestCase:
    """A single test case for a problem."""
    inputs: dict           # Parameter name -> value (JSON-serializable)
    expected: Any          # Expected output (JSON-serializable)
    description: str      # Human-readable description
    is_hidden: bool = False  # Hidden tests are not shown in the UI until run

    def input_repr(self) -> str:
        """Format inputs for display, e.g. 'nums = [2,7,11,15], target = 9'."""
        parts = []
        for k, v in self.inputs.items():
            parts.append(f"{k} = {_format_value(v)}")
        return ", ".join(parts)


def _format_value(v) -> str:
    """Format a value for human-readable display."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, (list, tuple)):
        items = ", ".join(_format_value(item) for item in v)
        return f"[{items}]"
    if isinstance(v, dict):
        items = ", ".join(f"{_format_value(k)}: {_format_value(val)}" for k, val in v.items())
        return "{" + items + "}"
    return str(v)


@dataclass
class ParamConstraints:
    """Constraints for random parameter generation."""
    min_val: Optional[int] = None
    max_val: Optional[int] = None
    min_len: Optional[int] = None
    max_len: Optional[int] = None
    unique: bool = False
    sorted: bool = False
    negative: bool = True
    allow_empty: bool = True
    allow_single: bool = True


@dataclass
class WrapperTemplate:
    """Template for generating execution wrappers.

    Attributes:
        template_str: Main execution template with {placeholders}.
        helpers_str: Helper code (ListNode, TreeNode classes, etc.).
        imports_str: Import statements needed by the template.
    """
    template_str: str = ""
    helpers_str: str = ""
    imports_str: str = ""


@dataclass
class ProblemInfo:
    """Lightweight problem summary (no test cases) for listing."""
    problem_id: str
    title: str
    method_name: str
    difficulty: str
    pattern: str
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "problem_id": self.problem_id,
            "title": self.title,
            "method_name": self.method_name,
            "difficulty": self.difficulty,
            "pattern": self.pattern,
            "description": self.description,
        }


class RandomGenerator(ABC):
    """Base class for random test case generators."""

    @abstractmethod
    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        """
        Generate random test cases.

        Args:
            count: Number of test cases to generate.
            constraints: Optional parameter constraints.

        Returns:
            List of TestCase objects.
        """
        pass


class Validator(ABC):
    """Base class for output validators."""

    @abstractmethod
    def validate(self, actual, expected) -> 'ValidationResult':
        """
        Validate that actual output matches expected output.

        Args:
            actual: The actual output from the solution.
            expected: The expected output.

        Returns:
            ValidationResult with pass/fail and details.
        """
        pass


@dataclass
class ValidationResult:
    """Result of validating a solution's output."""
    passed: bool
    expected_repr: str
    actual_repr: str
    diff_summary: str = ""


class ProblemPlugin(ABC):
    """
    Abstract base class for problem plugins.

    Every LeetCode problem is represented by a plugin that provides:
    - Problem metadata (id, title, difficulty, pattern)
    - Test cases (visible examples + hidden tests)
    - A validator for comparing outputs
    - Optional: random generator, wrapper template, parameter constraints

    Required methods: get_test_cases, get_validator
    Optional overrides: get_random_generator, get_wrapper_template, get_param_constraints
    """

    # Required metadata (set as class attributes in subclasses)
    problem_id: str = ""
    title: str = ""
    method_name: str = ""
    difficulty: str = "Easy"  # Easy, Medium, Hard
    pattern: str = ""         # DSA pattern category
    description: str = ""

    @abstractmethod
    def get_test_cases(self) -> list:
        """Return a list of TestCase objects for this problem."""
        pass

    @abstractmethod
    def get_validator(self) -> Validator:
        """Return a Validator instance for this problem."""
        pass

    def get_random_generator(self) -> Optional[RandomGenerator]:
        """Return a RandomGenerator, or None if random tests are not supported."""
        return None

    def get_wrapper_template(self) -> Optional[WrapperTemplate]:
        """Return a custom WrapperTemplate, or None to use auto-detection."""
        return None

    def get_param_constraints(self) -> Optional[dict]:
        """
        Return a dict of parameter_name -> ParamConstraints.
        Used by random generators to produce valid inputs.
        """
        return None

    def to_info(self) -> ProblemInfo:
        """Return a lightweight ProblemInfo summary."""
        return ProblemInfo(
            problem_id=self.problem_id,
            title=self.title,
            method_name=self.method_name,
            difficulty=self.difficulty,
            pattern=self.pattern,
            description=self.description,
        )
