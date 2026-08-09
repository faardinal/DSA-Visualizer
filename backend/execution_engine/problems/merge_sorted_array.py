"""
Merge Sorted Array problem plugin.
Pattern: Two Pointers
Difficulty: Easy

In-place problem: merges nums2 into nums1 in-place.
The validator must compare the mutated nums1 after execution.
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
    WrapperTemplate,
)


class MergeSortedArrayPlugin(ProblemPlugin):
    problem_id = "merge-sorted-array"
    leetcode_number = 88
    slug = "merge-sorted-array"
    title = "Merge Sorted Array"
    method_name = "merge"
    difficulty = "Easy"
    pattern = "Two Pointers"
    topics = ["Array", "Two Pointers", "Sorting"]
    parameters = ["nums1: List[int]", "m: int", "nums2: List[int]", "n: int"]
    return_type = "None"
    mutation_strategy = "nums1"
    hidden_test_count = 1
    description = (
        "Given two integer arrays nums1 and nums2 sorted in ascending order, "
        "merge nums2 into nums1 as one sorted array in-place."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={
                    "nums1": [1, 2, 3, 0, 0, 0],
                    "m": 3,
                    "nums2": [2, 5, 6],
                    "n": 3,
                },
                expected=[1, 2, 2, 3, 5, 6],
                description="Example 1",
                is_hidden=False,
            ),
            TestCase(
                inputs={
                    "nums1": [1],
                    "m": 1,
                    "nums2": [],
                    "n": 0,
                },
                expected=[1],
                description="Example 2: nums2 empty",
                is_hidden=False,
            ),
            TestCase(
                inputs={
                    "nums1": [0],
                    "m": 0,
                    "nums2": [1],
                    "n": 1,
                },
                expected=[1],
                description="Example 3: nums1 empty",
                is_hidden=False,
            ),
            TestCase(
                inputs={
                    "nums1": [4, 0, 0, 0, 0, 0],
                    "m": 1,
                    "nums2": [1, 2, 3, 5, 6],
                    "n": 5,
                },
                expected=[1, 2, 3, 4, 5, 6],
                description="Hidden: nums1 single element",
                is_hidden=True,
            ),
        ]

    def get_validator(self):
        return InPlaceValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(
            template_str=IN_PLACE_TEMPLATE,
            helpers_str="",
            imports_str="",
        )

    @staticmethod
    def oracle(inputs):
        return sorted(inputs["nums1"][:inputs["m"]] + inputs["nums2"][:inputs["n"]])

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            m, n = rng.randint(0, 20), rng.randint(0, 20)
            left = sorted(rng.randint(-50, 50) for _ in range(m))
            right = sorted(rng.randint(-50, 50) for _ in range(n))
            tests.append({"nums1": left + [0] * n, "m": m, "nums2": right, "n": n})
        return tests


IN_PLACE_TEMPLATE = """
# === Solution code ===
{solution_code}

# === Test execution ===
def main():
    # Build inputs (copy for in-place validation)
    nums1 = {nums1}
    m = {m}
    nums2 = {nums2}
    n = {n}

    # Capture state before
    import copy
    nums1_before = copy.deepcopy(nums1)

    sol = Solution()
    sol.merge(nums1, m, nums2, n)

    # Result is the mutated nums1
    result = nums1
    print(f"__RESULT__:\\n{repr(result)}")
    print(f"__INPUT_BEFORE__:\\n{repr(nums1_before)}")
    print(f"__INPUT_AFTER__:\\n{repr(nums1)}")

main()
"""


class InPlaceValidator(Validator):
    """
    Validator for in-place problems.
    Compares the actual mutated result against the expected result.
    The wrapper already captures the mutated state as the "result".
    """

    def validate(self, actual, expected):
        actual_repr = repr(actual)
        expected_repr = repr(expected)
        passed = actual == expected
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)
