"""
Shared validators for problem plugins.
Imported by problem files as needed.
"""
from backend.execution_engine.plugin_base import Validator, ValidationResult


class EqualityValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r}, got {actual!r}")


class SortedListValidator(Validator):
    """Validates list equality after sorting both sides."""
    def validate(self, actual, expected, inputs=None):
        try:
            a = sorted(actual) if actual is not None else []
            e = sorted(expected) if expected is not None else []
            passed = a == e
        except TypeError:
            passed = actual == expected
            a, e = actual, expected
        return ValidationResult(passed, repr(e), repr(a),
                                "" if passed else f"Expected {e!r} (sorted), got {a!r} (sorted)")


class SetValidator(Validator):
    """Validates list equality as sets (unordered, no duplicates)."""
    def validate(self, actual, expected, inputs=None):
        try:
            passed = set(actual or []) == set(expected or [])
        except TypeError:
            passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r} as set, got {actual!r}")


class AnyOrderListValidator(Validator):
    """Validates lists of lists where inner lists may be in any order."""
    def validate(self, actual, expected, inputs=None):
        try:
            a = sorted(tuple(sorted(row)) for row in (actual or []))
            e = sorted(tuple(sorted(row)) for row in (expected or []))
            passed = a == e
        except (TypeError, AttributeError):
            passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r}, got {actual!r}")


class BoolValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        passed = bool(actual) == bool(expected)
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r}, got {actual!r}")


class FloatValidator(Validator):
    def __init__(self, tol=1e-5):
        self.tol = tol

    def validate(self, actual, expected, inputs=None):
        try:
            passed = abs(float(actual) - float(expected)) <= self.tol
        except (TypeError, ValueError):
            passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r} ± {self.tol}, got {actual!r}")


class StringValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        passed = str(actual) == str(expected)
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r}, got {actual!r}")


class NullableEqualityValidator(Validator):
    """Accepts None or correct answer (for problems where None is valid empty)."""
    def validate(self, actual, expected, inputs=None):
        if expected is None:
            passed = actual is None or actual == []
        else:
            passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected {expected!r}, got {actual!r}")


class MultisetValidator(Validator):
    """Validates that two lists contain the same elements (same counts, any order)."""
    def validate(self, actual, expected, inputs=None):
        from collections import Counter
        try:
            passed = Counter(actual or []) == Counter(expected or [])
        except TypeError:
            passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected multiset {expected!r}, got {actual!r}")
