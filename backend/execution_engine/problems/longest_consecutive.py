from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator

class LongestConsecutivePlugin(ProblemPlugin):
    problem_id = "longest-consecutive-sequence"
    leetcode_number = 128
    slug = "longest-consecutive-sequence"
    title = "Longest Consecutive Sequence"
    method_name = "longestConsecutive"
    difficulty = "Medium"
    pattern = "Hashing"
    topics = ["Array", "Hash Table", "Union Find"]
    parameters = ["nums: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence."

    def get_test_cases(self):
        return [
            TestCase({"nums": [100,4,200,1,3,2]}, 4, "Example 1"),
            TestCase({"nums": [0,3,7,2,5,8,4,6,0,1]}, 9, "Example 2"),
            TestCase({"nums": []}, 0, "Empty array", is_hidden=True),
            TestCase({"nums": [1]}, 1, "Single element", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums = set(inputs["nums"])
        best = 0
        for n in nums:
            if n - 1 not in nums:
                cur = n
                length = 1
                while cur + 1 in nums:
                    cur += 1
                    length += 1
                best = max(best, length)
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            base = rng.randint(-20, 20)
            seq_len = rng.randint(2, 10)
            seq = list(range(base, base + seq_len))
            noise = [rng.randint(-50, 50) for _ in range(rng.randint(3, 10))]
            nums = seq + noise
            rng.shuffle(nums)
            tests.append({"nums": nums})
        return tests
