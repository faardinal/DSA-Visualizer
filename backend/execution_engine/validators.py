"""
Output validators for the execution engine.
Each validator compares actual vs expected output using appropriate comparison logic.
Validators are stateless and reusable.
"""

import math
from typing import Any

from .plugin_base import Validator, ValidationResult


class EqualityValidator(Validator):
    """Exact equality comparison (==)."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)
        passed = actual == expected
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class UnorderedValidator(Validator):
    """Unordered collection comparison — order doesn't matter."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)

        passed = _unordered_equal(actual, expected)
        diff = "" if passed else f"Contents differ. Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class FloatToleranceValidator(Validator):
    """Comparison with floating point tolerance."""

    def __init__(self, tolerance: float = 1e-5):
        self.tolerance = tolerance

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)

        passed = _float_equal(actual, expected, self.tolerance)
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr} (tolerance={self.tolerance})"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class TreeValidator(Validator):
    """Compare binary trees by serializing both to level-order lists."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)

        # If both are lists (already serialized), compare directly
        if isinstance(actual, list) and isinstance(expected, list):
            passed = _tree_lists_equal(actual, expected)
        else:
            passed = actual == expected

        diff = "" if passed else f"Tree structures differ. Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class LinkedListValidator(Validator):
    """Compare linked lists by serializing both to lists."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)

        # If both are lists (already serialized), compare directly
        if isinstance(actual, list) and isinstance(expected, list):
            passed = _tree_lists_equal(actual, expected)  # Same logic (handles None)
        else:
            passed = actual == expected

        diff = "" if passed else f"Linked lists differ. Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class GraphValidator(Validator):
    """Compare graph adjacency representations."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)

        passed = _graph_equal(actual, expected)
        diff = "" if passed else f"Graphs differ. Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class MatrixValidator(Validator):
    """Element-by-element 2D matrix comparison."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)

        passed = _matrix_equal(actual, expected)
        diff = "" if passed else f"Matrices differ. Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class InPlaceValidator(Validator):
    """
    Validator for in-place mutation problems.
    The wrapper captures the mutated state as the "result".
    Simply compares actual (mutated) with expected.
    """

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)
        passed = actual == expected
        diff = "" if passed else f"After mutation: expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class BoolValidator(Validator):
    """Boolean comparison with type coercion."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)
        passed = bool(actual) == bool(expected)
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


class IntValidator(Validator):
    """Integer comparison."""

    def validate(self, actual, expected) -> ValidationResult:
        actual_repr = _repr(actual)
        expected_repr = _repr(expected)
        try:
            passed = int(actual) == int(expected)
        except (TypeError, ValueError):
            passed = False
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def validator_for(plugin_or_name) -> Validator:
    """
    Create a validator from a plugin or validator name string.
    Plugins provide their own validator via get_validator().
    """
    if hasattr(plugin_or_name, "get_validator"):
        return plugin_or_name.get_validator()

    name = str(plugin_or_name)
    _VALIDATOR_MAP = {
        "equality": EqualityValidator,
        "unordered": UnorderedValidator,
        "float": FloatToleranceValidator,
        "tree": TreeValidator,
        "linked_list": LinkedListValidator,
        "graph": GraphValidator,
        "matrix": MatrixValidator,
        "in_place": InPlaceValidator,
        "bool": BoolValidator,
        "int": IntValidator,
    }

    cls = _VALIDATOR_MAP.get(name, EqualityValidator)
    return cls()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _repr(value) -> str:
    """Produce a clean repr for display."""
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    return repr(value)


def _unordered_equal(a, b) -> bool:
    """Compare two collections ignoring order."""
    try:
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            return sorted(a, key=_sort_key) == sorted(b, key=_sort_key)
        if isinstance(a, dict) and isinstance(b, dict):
            return (sorted(a.items(), key=_sort_key)
                    == sorted(b.items(), key=_sort_key))
        return a == b
    except TypeError:
        return False


def _sort_key(v):
    """Key for sorting heterogeneous values."""
    if isinstance(v, (int, float)):
        return (0, v, "")
    if isinstance(v, str):
        return (1, 0, v)
    return (2, 0, repr(v))


def _float_equal(a, b, tol=1e-5) -> bool:
    """Compare with float tolerance."""
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return a == b


def _tree_lists_equal(a: list, b: list) -> bool:
    """
    Compare two level-order tree representations.
    Handles trailing None differences gracefully.
    """
    if a == b:
        return True
    # Strip trailing None values and compare
    while a and a[-1] is None:
        a = a[:-1]
    while b and b[-1] is None:
        b = b[:-1]
    return a == b


def _graph_equal(a, b) -> bool:
    """Compare graph adjacency representations."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        for k in a:
            if sorted(a[k]) != sorted(b[k]):
                return False
        return True
    return a == b


def _matrix_equal(a, b) -> bool:
    """Compare 2D matrices element by element."""
    if not isinstance(a, list) or not isinstance(b, list):
        return a == b
    if len(a) != len(b):
        return False
    for row_a, row_b in zip(a, b):
        if len(row_a) != len(row_b):
            return False
        for ea, eb in zip(row_a, row_b):
            if ea != eb:
                return False
    return True
