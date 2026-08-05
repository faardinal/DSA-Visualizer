"""
Random test case generators for the execution engine.

Each generator produces TestCase objects with edge cases, large inputs,
and random data. Used by plugins to augment their fixed test cases.
"""

import random
from typing import Optional

from .plugin_base import (
    RandomGenerator, TestCase, ParamConstraints,
)


class ArrayRandomGenerator(RandomGenerator):
    """Generate random array test cases with edge cases."""

    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        c = constraints or ParamConstraints()
        tests = []

        # Edge cases
        if c.allow_empty:
            tests.append(self._make([],
                description="Empty array", constraints=c))
        if c.allow_single:
            tests.append(self._make([0],
                description="Single element", constraints=c))
            tests.append(self._make([1],
                description="Single element (1)", constraints=c))

        # Sorted variants
        if c.sorted or not c.unique:
            tests.append(self._make(sorted(random.sample(range(-10, 20), min(10, 20))),
                description="Sorted array", constraints=c))
            tests.append(self._make(list(reversed(sorted(random.sample(range(-10, 20), min(8, 20))))),
                description="Reverse sorted", constraints=c))

        # Duplicates
        tests.append(self._make([random.randint(0, 5) for _ in range(10)],
            description="Many duplicates", constraints=c))

        # Negative numbers
        if c.negative:
            tests.append(self._make([random.randint(-100, -1) for _ in range(8)],
                description="All negative", constraints=c))

        # Large case
        if c.max_len and c.max_len > 20:
            size = min(c.max_len, 1000)
            lo = c.min_val if c.min_val is not None else -10000
            hi = c.max_val if c.max_val is not None else 10000
            tests.append(self._make([random.randint(lo, hi) for _ in range(size)],
                description=f"Large array ({size} elements)", constraints=c))

        # Random cases to fill count
        while len(tests) < count:
            lo = c.min_val if c.min_val is not None else -100
            hi = c.max_val if c.max_val is not None else 100
            size = random.randint(c.min_len or 1, min(c.max_len or 20, 50))
            if c.unique and hi - lo + 1 >= size:
                arr = random.sample(range(lo, hi + 1), size)
            else:
                arr = [random.randint(lo, hi) for _ in range(size)]
            tests.append(self._make(arr, description="Random", constraints=c))

        return tests[:count]

    def _make(self, arr, description="", constraints=None):
        """Create a test case from an array. Override in subclasses."""
        return TestCase(
            inputs={"nums": arr},
            expected=None,  # Caller must compute expected
            description=description,
            is_hidden=True,
        )


class StringRandomGenerator(RandomGenerator):
    """Generate random string test cases."""

    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        c = constraints or ParamConstraints()
        tests = []

        if c.allow_empty:
            tests.append(TestCase(inputs={"s": ""}, expected=None,
                                  description="Empty string", is_hidden=True))
        if c.allow_single:
            tests.append(TestCase(inputs={"s": "a"}, expected=None,
                                  description="Single char", is_hidden=True))

        # Palindromes
        tests.append(TestCase(inputs={"s": "racecar"}, expected=None,
                              description="Palindrome", is_hidden=True))
        tests.append(TestCase(inputs={"s": "abba"}, expected=None,
                              description="Even palindrome", is_hidden=True))

        # Random strings
        chars = "abcdefghijklmnopqrstuvwxyz"
        while len(tests) < count:
            length = random.randint(1, min(c.max_len or 20, 50))
            s = "".join(random.choice(chars) for _ in range(length))
            tests.append(TestCase(inputs={"s": s}, expected=None,
                                  description="Random string", is_hidden=True))

        return tests[:count]


class LinkedListRandomGenerator(RandomGenerator):
    """Generate random linked list test cases."""

    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        c = constraints or ParamConstraints()
        tests = []

        if c.allow_empty:
            tests.append(TestCase(inputs={"head": []}, expected=None,
                                  description="Empty list", is_hidden=True))
        if c.allow_single:
            tests.append(TestCase(inputs={"head": [1]}, expected=None,
                                  description="Single node", is_hidden=True))

        # Random lists
        while len(tests) < count:
            lo = c.min_val if c.min_val is not None else -100
            hi = c.max_val if c.max_val is not None else 100
            size = random.randint(1, min(c.max_len or 10, 30))
            arr = [random.randint(lo, hi) for _ in range(size)]
            tests.append(TestCase(inputs={"head": arr}, expected=None,
                                  description="Random list", is_hidden=True))

        return tests[:count]


class TreeRandomGenerator(RandomGenerator):
    """Generate random binary tree test cases."""

    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        c = constraints or ParamConstraints()
        tests = []

        if c.allow_empty:
            tests.append(TestCase(inputs={"root": []}, expected=None,
                                  description="Empty tree", is_hidden=True))
        if c.allow_single:
            tests.append(TestCase(inputs={"root": [1]}, expected=None,
                                  description="Single node", is_hidden=True))

        # Complete tree
        tests.append(TestCase(inputs={"root": [1, 2, 3, 4, 5, 6, 7]}, expected=None,
                              description="Complete tree", is_hidden=True))

        # Skewed tree
        tests.append(TestCase(inputs={"root": [1, None, 2, None, 3, None, 4]}, expected=None,
                              description="Right-skewed", is_hidden=True))

        # Random trees (as level-order arrays with nulls)
        while len(tests) < count:
            size = random.randint(1, min(c.max_len or 15, 31))
            arr = []
            for i in range(size):
                if random.random() < 0.3:
                    arr.append(None)
                else:
                    lo = c.min_val if c.min_val is not None else -100
                    hi = c.max_val if c.max_val is not None else 100
                    arr.append(random.randint(lo, hi))
            arr[0] = random.randint(1, 100)  # Root must exist
            tests.append(TestCase(inputs={"root": arr}, expected=None,
                                  description="Random tree", is_hidden=True))

        return tests[:count]


class GraphRandomGenerator(RandomGenerator):
    """Generate random graph test cases."""

    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        c = constraints or ParamConstraints()
        tests = []

        # Empty graph
        tests.append(TestCase(inputs={"grid": [[]]}, expected=None,
                              description="Empty graph", is_hidden=True))
        # Single node
        tests.append(TestCase(inputs={"grid": [["1"]]}, expected=None,
                              description="Single node", is_hidden=True))
        # Small connected
        tests.append(TestCase(inputs={
            "grid": [["1", "1"], ["1", "1"]]
        }, expected=None, description="2x2 all land", is_hidden=True))

        # Random grids
        while len(tests) < count:
            rows = random.randint(1, min(c.max_len or 5, 10))
            cols = random.randint(1, min(c.max_len or 5, 10))
            grid = [[random.choice(["0", "1"]) for _ in range(cols)] for _ in range(rows)]
            tests.append(TestCase(inputs={"grid": grid}, expected=None,
                                  description=f"Random {rows}x{cols} grid", is_hidden=True))

        return tests[:count]


class MatrixRandomGenerator(RandomGenerator):
    """Generate random matrix test cases."""

    def generate(self, count: int, constraints: Optional[ParamConstraints] = None) -> list:
        c = constraints or ParamConstraints()
        tests = []

        # Empty
        tests.append(TestCase(inputs={"matrix": []}, expected=None,
                              description="Empty matrix", is_hidden=True))
        # Single element
        tests.append(TestCase(inputs={"matrix": [[1]]}, expected=None,
                              description="1x1 matrix", is_hidden=True))
        # Identity-like
        tests.append(TestCase(inputs={"matrix": [[1, 0], [0, 1]]}, expected=None,
                              description="Identity 2x2", is_hidden=True))

        # Random
        while len(tests) < count:
            rows = random.randint(1, min(c.max_len or 5, 8))
            cols = random.randint(1, min(c.max_len or 5, 8))
            lo = c.min_val if c.min_val is not None else 0
            hi = c.max_val if c.max_val is not None else 10
            matrix = [[random.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]
            tests.append(TestCase(inputs={"matrix": matrix}, expected=None,
                                  description=f"Random {rows}x{cols}", is_hidden=True))

        return tests[:count]
