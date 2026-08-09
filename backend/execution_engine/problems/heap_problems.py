"""Heap / Priority Queue pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult


# ═══════════════════════════════════════════════════════════════════════════
# LC 703 — Kth Largest Element in a Stream  (stateful)
# ═══════════════════════════════════════════════════════════════════════════
_KTH_STREAM_TPL = """{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    k, nums = args[0][0], args[0][1]
    obj  = KthLargest(k, nums)
    for op, arg in zip(ops[1:], args[1:]):
        if op == "add":
            out.append(obj.add(arg[0]))
        else:
            out.append(None)
    print("__RESULT__:")
    print(repr(out))

main()
"""

class KthLargestStreamPlugin(ProblemPlugin):
    problem_id = "kth-largest-element-in-a-stream"
    leetcode_number = 703
    title = "Kth Largest Element in a Stream"
    slug = "kth-largest-element-in-a-stream"
    method_name = "add"
    difficulty = "Easy"
    pattern = "Heap / Priority Queue"
    topics = ["Tree", "Design", "Binary Search Tree", "Heap", "Binary Tree", "Data Stream"]
    parameters = ["val: int"]
    return_type = "int"
    hidden_test_count = 3
    stateful = True
    description = "Design a class to find the kth largest element in a stream."

    def get_test_cases(self):
        return [
            TestCase(
                {"ops":["KthLargest","add","add","add","add","add"],
                 "args":[[3,[4,5,8,2]],[3],[5],[10],[9],[4]]},
                [None,4,5,5,8,8], "Example 1"
            ),
            TestCase(
                {"ops":["KthLargest","add","add"],
                 "args":[[1,[]],[1],[2]]},
                [None,1,2], "k=1", is_hidden=True
            ),
        ]

    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_KTH_STREAM_TPL)

    @staticmethod
    def oracle(inputs):
        import heapq
        ops, args = inputs["ops"], inputs["args"]
        k, nums = args[0][0], args[0][1]
        heap = sorted(nums)[-k:] if nums else []
        heapq.heapify(heap)
        while len(heap) > k: heapq.heappop(heap)
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "add":
                heapq.heappush(heap, arg[0])
                if len(heap) > k: heapq.heappop(heap)
                out.append(heap[0] if len(heap)==k else None)
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            k = rng.randint(1, 4)
            nums = [rng.randint(1, 30) for _ in range(rng.randint(0, 8))]
            ops = ["KthLargest"]; args = [[k, nums]]
            for _ in range(rng.randint(3, 7)):
                ops.append("add"); args.append([rng.randint(1, 30)])
            tests.append({"ops": ops, "args": args})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 1046 — Last Stone Weight
# ═══════════════════════════════════════════════════════════════════════════
class LastStoneWeightPlugin(ProblemPlugin):
    problem_id = "last-stone-weight"
    leetcode_number = 1046
    title = "Last Stone Weight"
    slug = "last-stone-weight"
    method_name = "lastStoneWeight"
    difficulty = "Easy"
    pattern = "Heap / Priority Queue"
    topics = ["Array", "Heap (Priority Queue)"]
    parameters = ["stones: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = "We smash the two heaviest stones each turn. The last remaining stone weight (or 0)."

    def get_test_cases(self):
        return [
            TestCase({"stones": [2,7,4,1,8,1]}, 1, "Example 1"),
            TestCase({"stones": [1]}, 1, "Single stone"),
            TestCase({"stones": [2,2]}, 0, "Two equal"),
            TestCase({"stones": [3,3,3]}, 3, "Three equal", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        import heapq
        stones = [-s for s in inputs["stones"]]
        heapq.heapify(stones)
        while len(stones) > 1:
            a = -heapq.heappop(stones)
            b = -heapq.heappop(stones)
            if a != b: heapq.heappush(stones, -(a - b))
        return -stones[0] if stones else 0

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            tests.append({"stones": [rng.randint(1, 30) for _ in range(rng.randint(1, 12))]})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 973 — K Closest Points to Origin
# ═══════════════════════════════════════════════════════════════════════════
class KClosestPointsPlugin(ProblemPlugin):
    problem_id = "k-closest-points-to-origin"
    leetcode_number = 973
    title = "K Closest Points to Origin"
    slug = "k-closest-points-to-origin"
    method_name = "kClosest"
    difficulty = "Medium"
    pattern = "Heap / Priority Queue"
    topics = ["Array", "Math", "Divide and Conquer", "Geometry", "Sorting", "Heap"]
    parameters = ["points: List[List[int]]", "k: int"]
    return_type = "List[List[int]]"
    hidden_test_count = 4
    description = "Given an array of points, return the k closest points to the origin (0,0)."

    def get_test_cases(self):
        return [
            TestCase({"points": [[1,3],[-2,2]], "k": 1}, [[-2,2]], "Example 1"),
            TestCase({"points": [[3,3],[5,-1],[-2,4]], "k": 2}, [[3,3],[-2,4]], "Example 2"),
            TestCase({"points": [[0,1],[1,0]], "k": 2}, [[0,1],[1,0]], "Both equal dist", is_hidden=True),
        ]

    def get_validator(self):
        return KClosestValidator()

    @staticmethod
    def oracle(inputs):
        pts, k = inputs["points"], inputs["k"]
        return sorted(pts, key=lambda p: p[0]**2+p[1]**2)[:k]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 15)
            pts = [[rng.randint(-20,20), rng.randint(-20,20)] for _ in range(n)]
            k = rng.randint(1, n)
            tests.append({"points": pts, "k": k})
        return tests

class KClosestValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # Same set of points, any order
        try:
            a = sorted(tuple(p) for p in actual)
            e = sorted(tuple(p) for p in expected)
            passed = a == e
        except Exception:
            passed = False; a = actual; e = expected
        return ValidationResult(passed, repr(e), repr(a), "" if passed else "Points differ")


# ═══════════════════════════════════════════════════════════════════════════
# LC 215 — Kth Largest Element in an Array
# ═══════════════════════════════════════════════════════════════════════════
class KthLargestArrayPlugin(ProblemPlugin):
    problem_id = "kth-largest-element-in-an-array"
    leetcode_number = 215
    title = "Kth Largest Element in an Array"
    slug = "kth-largest-element-in-an-array"
    method_name = "findKthLargest"
    difficulty = "Medium"
    pattern = "Heap / Priority Queue"
    topics = ["Array", "Divide and Conquer", "Sorting", "Heap", "Quickselect"]
    parameters = ["nums: List[int]", "k: int"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given an integer array nums and an integer k, return the kth largest element in the array."

    def get_test_cases(self):
        return [
            TestCase({"nums": [3,2,1,5,6,4], "k": 2}, 5, "Example 1"),
            TestCase({"nums": [3,2,3,1,2,4,5,5,6], "k": 4}, 4, "Example 2"),
            TestCase({"nums": [1], "k": 1}, 1, "Single element"),
            TestCase({"nums": [2,1], "k": 2}, 1, "Two elements", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        return sorted(inputs["nums"], reverse=True)[inputs["k"]-1]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 20)
            nums = [rng.randint(-50, 50) for _ in range(n)]
            k = rng.randint(1, n)
            tests.append({"nums": nums, "k": k})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 621 — Task Scheduler
# ═══════════════════════════════════════════════════════════════════════════
class TaskSchedulerPlugin(ProblemPlugin):
    problem_id = "task-scheduler"
    leetcode_number = 621
    title = "Task Scheduler"
    slug = "task-scheduler"
    method_name = "leastInterval"
    difficulty = "Medium"
    pattern = "Heap / Priority Queue"
    topics = ["Array", "Hash Table", "Greedy", "Sorting", "Heap", "Counting"]
    parameters = ["tasks: List[str]", "n: int"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given a CPU task list and cooldown n, return the minimum intervals needed to finish all tasks."

    def get_test_cases(self):
        return [
            TestCase({"tasks": ["A","A","A","B","B","B"], "n": 2}, 8, "Example 1"),
            TestCase({"tasks": ["A","C","A","B","D","B"], "n": 1}, 6, "Example 2"),
            TestCase({"tasks": ["A","A","A","B","B","B"], "n": 3}, 10, "Example 3"),
            TestCase({"tasks": ["A"], "n": 0}, 1, "Single task", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import Counter
        tasks, n = inputs["tasks"], inputs["n"]
        counts = Counter(tasks)
        max_count = max(counts.values())
        max_count_tasks = sum(1 for v in counts.values() if v == max_count)
        return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            tasks = [rng.choice("ABCDEFGH") for _ in range(rng.randint(3, 20))]
            n = rng.randint(0, 4)
            tests.append({"tasks": tasks, "n": n})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 295 — Find Median from Data Stream  (stateful)
# ═══════════════════════════════════════════════════════════════════════════
_MEDIAN_STREAM_TPL = """{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = MedianFinder()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "addNum":
            obj.addNum(arg[0])
            out.append(None)
        elif op == "findMedian":
            out.append(obj.findMedian())
    print("__RESULT__:")
    print(repr(out))

main()
"""

class FindMedianFromStreamPlugin(ProblemPlugin):
    problem_id = "find-median-from-data-stream"
    leetcode_number = 295
    title = "Find Median from Data Stream"
    slug = "find-median-from-data-stream"
    method_name = "addNum"
    difficulty = "Hard"
    pattern = "Heap / Priority Queue"
    topics = ["Two Pointers", "Design", "Sorting", "Heap", "Data Stream"]
    parameters = ["num: int"]
    return_type = "None"
    hidden_test_count = 3
    stateful = True
    description = "Design a data structure that supports adding integers and finding the median."

    def get_test_cases(self):
        return [
            TestCase(
                {"ops":["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"],
                 "args":[[],[1],[2],[],[3],[]]},
                [None,None,None,1.5,None,2.0], "Example 1"
            ),
            TestCase(
                {"ops":["MedianFinder","addNum","findMedian"],
                 "args":[[],[5],[]]},
                [None,None,5.0], "Single element", is_hidden=True
            ),
        ]

    def get_validator(self):
        return MedianStreamValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_MEDIAN_STREAM_TPL)

    @staticmethod
    def oracle(inputs):
        ops, args = inputs["ops"], inputs["args"]
        nums = []
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "addNum":
                import bisect
                bisect.insort(nums, arg[0])
                out.append(None)
            elif op == "findMedian":
                n = len(nums)
                if n % 2: out.append(float(nums[n//2]))
                else: out.append((nums[n//2-1]+nums[n//2])/2.0)
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            ops=["MedianFinder"]; args=[[]]
            for _ in range(rng.randint(3,8)):
                ops.append("addNum"); args.append([rng.randint(-50,50)])
                if rng.random()>0.4:
                    ops.append("findMedian"); args.append([])
            tests.append({"ops":ops,"args":args})
        return tests

class MedianStreamValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        if len(actual) != len(expected):
            return ValidationResult(False, repr(expected), repr(actual), "Length mismatch")
        for a, e in zip(actual, expected):
            if a is None and e is None: continue
            if a is None or e is None:
                return ValidationResult(False, repr(expected), repr(actual), f"None mismatch: {a} vs {e}")
            if abs(float(a)-float(e)) > 1e-5:
                return ValidationResult(False, repr(expected), repr(actual), f"{a} != {e}")
        return ValidationResult(True, repr(expected), repr(actual), "")
