"""Two Pointer pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, AnyOrderListValidator, Validator, ValidationResult
)


# ---------------------------------------------------------------------------
# Valid Palindrome  (LC 125)
# ---------------------------------------------------------------------------
class ValidPalindromePlugin(ProblemPlugin):
    problem_id = "valid-palindrome"
    leetcode_number = 125
    slug = "valid-palindrome"
    title = "Valid Palindrome"
    method_name = "isPalindrome"
    difficulty = "Easy"
    pattern = "Two Pointers"
    topics = ["Two Pointers", "String"]
    parameters = ["s: str"]
    return_type = "bool"
    hidden_test_count = 4
    description = (
        "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters "
        "and removing all non-alphanumeric characters, it reads the same forward and backward."
    )

    def get_test_cases(self):
        return [
            TestCase({"s": "A man, a plan, a canal: Panama"}, True, "Example 1"),
            TestCase({"s": "race a car"}, False, "Example 2"),
            TestCase({"s": " "}, True, "Only spaces"),
            TestCase({"s": "abcba"}, True, "Simple palindrome", is_hidden=True),
            TestCase({"s": "abc"}, False, "Not palindrome", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s = "".join(c.lower() for c in inputs["s"] if c.isalnum())
        return s == s[::-1]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for i in range(count):
            chars = list(string.ascii_lowercase[:10] + string.digits[:5])
            if i % 2 == 0:
                half = [rng.choice(chars) for _ in range(rng.randint(1, 8))]
                s = "".join(half + half[::-1])
            else:
                s = "".join(rng.choice(chars) for _ in range(rng.randint(2, 14)))
            tests.append({"s": s})
        return tests


# ---------------------------------------------------------------------------
# Two Sum II (LC 167)
# ---------------------------------------------------------------------------
class TwoSumIIPlugin(ProblemPlugin):
    problem_id = "two-sum-ii-input-array-is-sorted"
    leetcode_number = 167
    slug = "two-sum-ii-input-array-is-sorted"
    title = "Two Sum II - Input Array Is Sorted"
    method_name = "twoSumII"
    difficulty = "Medium"
    pattern = "Two Pointers"
    topics = ["Array", "Two Pointers", "Binary Search"]
    parameters = ["numbers: List[int]", "target: int"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = (
        "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, "
        "find two numbers such that they add up to a specific target number."
    )

    def get_test_cases(self):
        return [
            TestCase({"numbers": [2,7,11,15], "target": 9}, [1,2], "Example 1"),
            TestCase({"numbers": [2,3,4], "target": 6}, [1,3], "Example 2"),
            TestCase({"numbers": [-1,0], "target": -1}, [1,2], "Example 3"),
            TestCase({"numbers": [1,2,3,4,5], "target": 9}, [4,5], "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums, target = inputs["numbers"], inputs["target"]
        l, r = 0, len(nums) - 1
        while l < r:
            s = nums[l] + nums[r]
            if s == target: return [l+1, r+1]
            elif s < target: l += 1
            else: r -= 1
        return []

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 20)
            nums = sorted(rng.randint(-50, 50) for _ in range(n))
            i, j = rng.sample(range(n), 2)
            if i > j: i, j = j, i
            tests.append({"numbers": nums, "target": nums[i] + nums[j]})
        return tests


# ---------------------------------------------------------------------------
# 3Sum  (LC 15)
# ---------------------------------------------------------------------------
class ThreeSumPlugin(ProblemPlugin):
    problem_id = "3sum"
    leetcode_number = 15
    slug = "3sum"
    title = "3Sum"
    method_name = "threeSum"
    difficulty = "Medium"
    pattern = "Two Pointers"
    topics = ["Array", "Two Pointers", "Sorting"]
    parameters = ["nums: List[int]"]
    return_type = "List[List[int]]"
    hidden_test_count = 4
    description = (
        "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] "
        "such that i != j, i != k, j != k, and nums[i] + nums[j] + nums[k] == 0."
    )

    def get_test_cases(self):
        return [
            TestCase({"nums": [-1,0,1,2,-1,-4]}, [[-1,-1,2],[-1,0,1]], "Example 1"),
            TestCase({"nums": [0,1,1]}, [], "Example 2"),
            TestCase({"nums": [0,0,0]}, [[0,0,0]], "Example 3"),
            TestCase({"nums": [-2,0,1,1,2]}, [[-2,0,2],[-2,1,1]], "Hidden", is_hidden=True),
        ]

    def get_validator(self): return AnyOrderListValidator()

    @staticmethod
    def oracle(inputs):
        nums = sorted(inputs["nums"])
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]: continue
            l, r = i+1, len(nums)-1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    result.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l+1]: l += 1
                    while l < r and nums[r] == nums[r-1]: r -= 1
                    l += 1; r -= 1
                elif s < 0: l += 1
                else: r -= 1
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(3, 15)
            nums = [rng.randint(-10, 10) for _ in range(n)]
            tests.append({"nums": nums})
        return tests


# ---------------------------------------------------------------------------
# Container With Most Water  (LC 11)
# ---------------------------------------------------------------------------
class ContainerWithMostWaterPlugin(ProblemPlugin):
    problem_id = "container-with-most-water"
    leetcode_number = 11
    slug = "container-with-most-water"
    title = "Container With Most Water"
    method_name = "maxArea"
    difficulty = "Medium"
    pattern = "Two Pointers"
    topics = ["Array", "Two Pointers", "Greedy"]
    parameters = ["height: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "You are given an integer array height of length n. Find two lines that together with "
        "the x-axis form a container, such that the container contains the most water."
    )

    def get_test_cases(self):
        return [
            TestCase({"height": [1,8,6,2,5,4,8,3,7]}, 49, "Example 1"),
            TestCase({"height": [1,1]}, 1, "Example 2"),
            TestCase({"height": [4,3,2,1,4]}, 16, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        h = inputs["height"]
        l, r = 0, len(h)-1
        best = 0
        while l < r:
            best = max(best, min(h[l], h[r]) * (r - l))
            if h[l] < h[r]: l += 1
            else: r -= 1
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 20)
            tests.append({"height": [rng.randint(1, 50) for _ in range(n)]})
        return tests


# ---------------------------------------------------------------------------
# Trapping Rain Water  (LC 42)
# ---------------------------------------------------------------------------
class TrappingRainWaterPlugin(ProblemPlugin):
    problem_id = "trapping-rain-water"
    leetcode_number = 42
    slug = "trapping-rain-water"
    title = "Trapping Rain Water"
    method_name = "trap"
    difficulty = "Hard"
    pattern = "Two Pointers"
    topics = ["Array", "Two Pointers", "Dynamic Programming", "Stack"]
    parameters = ["height: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Given n non-negative integers representing an elevation map where the width of each bar is 1, "
        "compute how much water it can trap after raining."
    )

    def get_test_cases(self):
        return [
            TestCase({"height": [0,1,0,2,1,0,1,3,2,1,2,1]}, 6, "Example 1"),
            TestCase({"height": [4,2,0,3,2,5]}, 9, "Example 2"),
            TestCase({"height": [1,0,1]}, 1, "Simple trap", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        h = inputs["height"]
        if not h: return 0
        l, r = 0, len(h)-1
        lmax, rmax = h[l], h[r]
        water = 0
        while l < r:
            if lmax < rmax:
                l += 1; lmax = max(lmax, h[l])
                water += lmax - h[l]
            else:
                r -= 1; rmax = max(rmax, h[r])
                water += rmax - h[r]
        return water

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(3, 18)
            tests.append({"height": [rng.randint(0, 8) for _ in range(n)]})
        return tests
