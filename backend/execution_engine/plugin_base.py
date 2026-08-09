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
from typing import Any, Callable, Optional


@dataclass
class TestCase:
    """A single test case for a problem."""
    inputs: dict           # Parameter name -> value (JSON-serializable)
    expected: Any          # Expected output (JSON-serializable)
    description: str      # Human-readable description
    is_hidden: bool = False  # Hidden tests are not shown in the UI until run
    test_id: Optional[str] = None
    seed: Optional[int] = None

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
    leetcode_number: Optional[int] = None
    slug: str = ""
    topics: list[str] = field(default_factory=list)
    starter_code: str = ""

    def to_dict(self) -> dict:
        return {
            "problem_id": self.problem_id,
            "title": self.title,
            "method_name": self.method_name,
            "difficulty": self.difficulty,
            "pattern": self.pattern,
            "description": self.description,
            "leetcode_number": self.leetcode_number,
            "slug": self.slug,
            "topics": self.topics,
            "starter_code": self.starter_code,
        }


def build_starter_code(method_name: str, parameters: list, return_type: str = "Any") -> str:
    """Generate a canonical LeetCode-style starter code snippet.

    Produces a class Solution with the correct method signature, the standard
    typing imports needed for List/Optional/etc., and a single ``pass`` body.
    """
    params_str = ", ".join(["self"] + list(parameters))
    combined = params_str + " " + (return_type or "")
    typing_names = [n for n in ("List", "Optional", "Dict", "Tuple", "Set", "Any") if n in combined]
    import_line = ("from typing import " + ", ".join(typing_names) + "\n\n") if typing_names else ""
    rt = return_type or "Any"
    method_sig = f"    def {method_name}({params_str}) -> {rt}:"
    return f"{import_line}class Solution:\n{method_sig}\n        pass\n"


@dataclass
class ProblemDefinition:
    """Complete, data-driven contract for a judged LeetCode problem.

    `generator` receives a dedicated ``random.Random`` instance and returns
    JSON-like parameter dictionaries or TestCase objects. `oracle` receives a
    deep-copied parameter dictionary, keeping expected answers independent of
    the submitted solution.
    """
    problem_id: str
    leetcode_number: int
    slug: str
    title: str
    difficulty: str
    topics: list[str]
    method_name: str
    parameters: list[str]
    return_type: str
    description: str
    examples: list[TestCase] = field(default_factory=list)
    constraints: str = ""
    input_schema: dict = field(default_factory=dict)
    output_schema: dict = field(default_factory=dict)
    generator: Optional[Callable] = None
    oracle: Optional[Callable] = None
    validator: Optional["Validator"] = None
    serialization: str = "json"
    mutation_strategy: Optional[str] = None
    stateful: bool = False
    hidden_test_count: int = 0


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
    leetcode_number: Optional[int] = None
    slug: str = ""
    topics: list[str] = []
    parameters: list[str] = []
    return_type: str = "Any"
    constraints: str = ""
    input_schema: dict = {}
    output_schema: dict = {}
    serialization: str = "json"
    mutation_strategy: Optional[str] = None
    stateful: bool = False

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

    def get_definition(self) -> ProblemDefinition:
        """Return a complete definition while keeping older plugins valid."""
        return ProblemDefinition(
            problem_id=self.problem_id,
            leetcode_number=self.leetcode_number or 0,
            slug=self.slug or self.problem_id,
            title=self.title,
            difficulty=self.difficulty,
            topics=list(self.topics),
            method_name=self.method_name,
            parameters=list(self.parameters),
            return_type=self.return_type,
            description=self.description,
            examples=[case for case in self.get_test_cases() if not case.is_hidden],
            constraints=self.constraints,
            input_schema=dict(self.input_schema),
            output_schema=dict(self.output_schema),
            generator=getattr(self, "generate_hidden_inputs", None),
            oracle=getattr(self, "oracle", None),
            validator=self.get_validator(),
            serialization=self.serialization,
            mutation_strategy=self.mutation_strategy,
            stateful=self.stateful,
            hidden_test_count=getattr(self, "hidden_test_count", 0),
        )

    def build_test_cases(self, rng, seed: int) -> list[TestCase]:
        """Build deterministic tests and calculate generated expected values.

        Older plugins continue to return their curated tests. New definitions
        can supply a generator and oracle without duplicating expected outputs.
        """
        definition = self.get_definition()
        tests = list(definition.examples) if definition.generator else list(self.get_test_cases())
        if definition.generator is None:
            return tests

        generated = definition.generator(rng, definition.hidden_test_count)
        for index, generated_case in enumerate(generated):
            case = generated_case if isinstance(generated_case, TestCase) else TestCase(
                inputs=generated_case,
                expected=None,
                description=f"Hidden test {index + 1}",
                is_hidden=True,
            )
            if definition.oracle is None:
                raise ValueError(f"Problem '{self.problem_id}' has a generator but no oracle.")
            case.expected = definition.oracle(case.inputs.copy())
            case.is_hidden = True
            case.seed = seed
            case.test_id = case.test_id or f"generated-{index}"
            tests.append(case)
        return tests

    def to_info(self) -> ProblemInfo:
        """Return a lightweight ProblemInfo summary."""
        return ProblemInfo(
            problem_id=self.problem_id,
            title=self.title,
            method_name=self.method_name,
            difficulty=self.difficulty,
            pattern=self.pattern,
            description=self.description,
            leetcode_number=self.leetcode_number,
            slug=self.slug or self.problem_id,
            topics=list(self.topics),
            starter_code=build_starter_code(
                self.method_name,
                list(self.parameters),
                self.return_type,
            ),
        )
