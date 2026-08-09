"""Binary Search pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator, FloatValidator


# ---------------------------------------------------------------------------
# Search a 2D Matrix  (LC 74)
# ---------------------------------------------------------------------------
class SearchMatrix2DPlugin(ProblemPlugin):
    problem_id = "search-a-2d-matrix"
    leetcode_number = 74
    slug = "search-a-2d-matrix"
    title = "Search a 2D Matrix"
    method_name = "searchMatrix"
    difficulty = "Medium"
    pattern = "Binary Search"
    topics = ["Array", "Binary Search", "Matrix"]
    parameters = ["matrix: List[List[int]]", "target: int"]
    return_type = "bool"
    hidden_test_count = 4
    description = (
        "You are given an m x n integer matrix matrix with sorted rows. "
        "Given an integer target, return true if target is in matrix or false otherwise."
    )

    def get_test_cases(self):
        return [
            TestCase({"matrix": [[1,3,5,7],[10,11,16,20],[23,30,34,60]], "target": 3}, True, "Example 1"),
            TestCase({"matrix": [[1,3,5,7],[10,11,16,20],[23,30,34,60]], "target": 13}, False, "Example 2"),
            TestCase({"matrix": [[1]], "target": 1}, True, "Single element", is_hidden=True),
            TestCase({"matrix": [[1]], "target": 2}, False, "Single element miss", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        matrix, target = inputs["matrix"], inputs["target"]
        m, n = len(matrix), len(matrix[0]) if matrix else 0
        lo, hi = 0, m * n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            v = matrix[mid // n][mid % n]
            if v == target: return True
            elif v < target: lo = mid + 1
            else: hi = mid - 1
        return False

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            rows = rng.randint(1, 4)
            cols = rng.randint(1, 5)
            flat = sorted(rng.sample(range(1, 100), rows * cols))
            matrix = [flat[r*cols:(r+1)*cols] for r in range(rows)]
            if i % 2 == 0:
                target = flat[rng.randint(0, len(flat)-1)]
            else:
                target = rng.randint(101, 150)
            tests.append({"matrix": matrix, "target": target})
        return tests


# ---------------------------------------------------------------------------
# Koko Eating Bananas  (LC 875)
# ---------------------------------------------------------------------------
class KokoEatingBananasPlugin(ProblemPlugin):
    problem_id = "koko-eating-bananas"
    leetcode_number = 875
    slug = "koko-eating-bananas"
    title = "Koko Eating Bananas"
    method_name = "minEatingSpeed"
    difficulty = "Medium"
    pattern = "Binary Search"
    topics = ["Array", "Binary Search"]
    parameters = ["piles: List[int]", "h: int"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Koko loves bananas. Given piles where piles[i] is the number of bananas in the ith pile, "
        "and h hours, return the minimum integer k such that she can eat all bananas within h hours."
    )

    def get_test_cases(self):
        return [
            TestCase({"piles": [3,6,7,11], "h": 8}, 4, "Example 1"),
            TestCase({"piles": [30,11,23,4,20], "h": 5}, 30, "Example 2"),
            TestCase({"piles": [30,11,23,4,20], "h": 6}, 23, "Example 3"),
            TestCase({"piles": [1,1,1,1], "h": 4}, 1, "All ones", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        import math
        piles, h = inputs["piles"], inputs["h"]
        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if sum(math.ceil(p / mid) for p in piles) <= h:
                hi = mid
            else:
                lo = mid + 1
        return lo

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 8)
            piles = [rng.randint(1, 30) for _ in range(n)]
            h = rng.randint(n, n * 5)
            tests.append({"piles": piles, "h": h})
        return tests


# ---------------------------------------------------------------------------
# Find Minimum in Rotated Sorted Array  (LC 153)
# ---------------------------------------------------------------------------
class FindMinRotatedPlugin(ProblemPlugin):
    problem_id = "find-minimum-in-rotated-sorted-array"
    leetcode_number = 153
    slug = "find-minimum-in-rotated-sorted-array"
    title = "Find Minimum in Rotated Sorted Array"
    method_name = "findMin"
    difficulty = "Medium"
    pattern = "Binary Search"
    topics = ["Array", "Binary Search"]
    parameters = ["nums: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Given the sorted rotated array nums of unique elements, return the minimum element of this array."
    )

    def get_test_cases(self):
        return [
            TestCase({"nums": [3,4,5,1,2]}, 1, "Example 1"),
            TestCase({"nums": [4,5,6,7,0,1,2]}, 0, "Example 2"),
            TestCase({"nums": [11,13,15,17]}, 11, "Example 3: not rotated"),
            TestCase({"nums": [2,1]}, 1, "Two elements", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums = inputs["nums"]
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]: lo = mid + 1
            else: hi = mid
        return nums[lo]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 15)
            nums = sorted(rng.sample(range(-50, 50), n))
            k = rng.randint(0, n - 1)
            tests.append({"nums": nums[k:] + nums[:k]})
        return tests


# ---------------------------------------------------------------------------
# Search in Rotated Sorted Array  (LC 33)
# ---------------------------------------------------------------------------
class SearchRotatedSortedArrayPlugin(ProblemPlugin):
    problem_id = "search-in-rotated-sorted-array"
    leetcode_number = 33
    slug = "search-in-rotated-sorted-array"
    title = "Search in Rotated Sorted Array"
    method_name = "searchRotated"
    difficulty = "Medium"
    pattern = "Binary Search"
    topics = ["Array", "Binary Search"]
    parameters = ["nums: List[int]", "target: int"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Given the array nums after the possible rotation and an integer target, "
        "return the index of target if it is in nums, or -1 if it is not in nums."
    )

    def get_test_cases(self):
        return [
            TestCase({"nums": [4,5,6,7,0,1,2], "target": 0}, 4, "Example 1"),
            TestCase({"nums": [4,5,6,7,0,1,2], "target": 3}, -1, "Example 2"),
            TestCase({"nums": [1], "target": 0}, -1, "Example 3"),
            TestCase({"nums": [1,3], "target": 3}, 1, "Two elements", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums, target = inputs["nums"], inputs["target"]
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target: return mid
            if nums[lo] <= nums[mid]:
                if nums[lo] <= target < nums[mid]: hi = mid - 1
                else: lo = mid + 1
            else:
                if nums[mid] < target <= nums[hi]: lo = mid + 1
                else: hi = mid - 1
        return -1

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            n = rng.randint(2, 15)
            nums = sorted(rng.sample(range(-50, 50), n))
            k = rng.randint(0, n - 1)
            rotated = nums[k:] + nums[:k]
            if i % 2 == 0:
                target = rotated[rng.randint(0, n-1)]
            else:
                target = rng.randint(51, 80)
            tests.append({"nums": rotated, "target": target})
        return tests


# ---------------------------------------------------------------------------
# Time Based Key-Value Store  (LC 981) — stateful
# ---------------------------------------------------------------------------
_TIME_KV_WRAPPER = '''
{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = TimeMap()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "set":
            obj.set(arg[0], arg[1], arg[2])
            out.append(None)
        elif op == "get":
            out.append(obj.get(arg[0], arg[1]))
    print("__RESULT__:")
    print(repr(out))

main()
'''

class TimeBasedKVStorePlugin(ProblemPlugin):
    problem_id = "time-based-key-value-store"
    leetcode_number = 981
    slug = "time-based-key-value-store"
    title = "Time Based Key-Value Store"
    method_name = "set"
    difficulty = "Medium"
    pattern = "Binary Search"
    topics = ["Hash Table", "String", "Binary Search", "Design"]
    parameters = ["key: str", "value: str", "timestamp: int"]
    return_type = "None"
    hidden_test_count = 3
    stateful = True
    description = (
        "Design a time-based key-value data structure that can store multiple values for the same key "
        "at different time stamps and retrieve the key's value at a certain timestamp."
    )

    def get_test_cases(self):
        return [
            TestCase(
                {"ops": ["TimeMap","set","get","get","set","get","get"],
                 "args": [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]},
                [None,None,"bar","bar",None,"bar2","bar2"],
                "Example 1"
            ),
            TestCase(
                {"ops": ["TimeMap","set","get","get"],
                 "args": [[],["love","high",10],["love",5],["love",10]]},
                [None,None,"","high"],
                "Hidden: before earliest time", is_hidden=True
            ),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_TIME_KV_WRAPPER)

    @staticmethod
    def oracle(inputs):
        from collections import defaultdict
        import bisect
        ops, args = inputs["ops"], inputs["args"]
        store = defaultdict(list)
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "set":
                store[arg[0]].append((arg[2], arg[1]))
                out.append(None)
            elif op == "get":
                key, ts = arg[0], arg[1]
                times = store[key]
                lo, hi = 0, len(times) - 1
                res = ""
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if times[mid][0] <= ts:
                        res = times[mid][1]; lo = mid + 1
                    else:
                        hi = mid - 1
                out.append(res)
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        from backend.execution_engine.plugin_base import WrapperTemplate
        for _ in range(count):
            ops = ["TimeMap"]; args = [[]]
            keys = ["a","b","c"]
            ts = 1
            for _ in range(rng.randint(3, 7)):
                k = rng.choice(keys)
                v = rng.choice(["x","y","z"])
                ops.append("set"); args.append([k, v, ts]); ts += rng.randint(1, 5)
            for _ in range(rng.randint(2, 4)):
                k = rng.choice(keys)
                t = rng.randint(1, ts)
                ops.append("get"); args.append([k, t])
            tests.append({"ops": ops, "args": args})
        return tests


# ---------------------------------------------------------------------------
# Median of Two Sorted Arrays  (LC 4)
# ---------------------------------------------------------------------------
class MedianTwoSortedArraysPlugin(ProblemPlugin):
    problem_id = "median-of-two-sorted-arrays"
    leetcode_number = 4
    slug = "median-of-two-sorted-arrays"
    title = "Median of Two Sorted Arrays"
    method_name = "findMedianSortedArrays"
    difficulty = "Hard"
    pattern = "Binary Search"
    topics = ["Array", "Binary Search", "Divide and Conquer"]
    parameters = ["nums1: List[int]", "nums2: List[int]"]
    return_type = "float"
    hidden_test_count = 4
    description = (
        "Given two sorted arrays nums1 and nums2 of size m and n respectively, "
        "return the median of the two sorted arrays."
    )

    def get_test_cases(self):
        return [
            TestCase({"nums1": [1,3], "nums2": [2]}, 2.0, "Example 1"),
            TestCase({"nums1": [1,2], "nums2": [3,4]}, 2.5, "Example 2"),
            TestCase({"nums1": [], "nums2": [1]}, 1.0, "One empty", is_hidden=True),
            TestCase({"nums1": [2], "nums2": []}, 2.0, "Other empty", is_hidden=True),
        ]

    def get_validator(self): return FloatValidator(tol=1e-5)

    @staticmethod
    def oracle(inputs):
        merged = sorted(inputs["nums1"] + inputs["nums2"])
        n = len(merged)
        if n % 2: return float(merged[n // 2])
        return (merged[n//2 - 1] + merged[n//2]) / 2.0

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            m = rng.randint(0, 8)
            n = rng.randint(0, 8)
            while m + n == 0: n = 1
            a = sorted(rng.randint(-20, 20) for _ in range(m))
            b = sorted(rng.randint(-20, 20) for _ in range(n))
            tests.append({"nums1": a, "nums2": b})
        return tests
