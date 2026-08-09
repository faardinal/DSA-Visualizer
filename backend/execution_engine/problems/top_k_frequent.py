from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import SetValidator

class TopKFrequentPlugin(ProblemPlugin):
    problem_id = "top-k-frequent-elements"
    leetcode_number = 347
    slug = "top-k-frequent-elements"
    title = "Top K Frequent Elements"
    method_name = "topKFrequent"
    difficulty = "Medium"
    pattern = "Hashing"
    topics = ["Array", "Hash Table", "Bucket Sort", "Heap"]
    parameters = ["nums: List[int]", "k: int"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = "Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order."

    def get_test_cases(self):
        return [
            TestCase({"nums": [1,1,1,2,2,3], "k": 2}, [1,2], "Example 1"),
            TestCase({"nums": [1], "k": 1}, [1], "Example 2"),
            TestCase({"nums": [1,2], "k": 2}, [1,2], "Both elements", is_hidden=True),
        ]

    def get_validator(self): return SetValidator()

    @staticmethod
    def oracle(inputs):
        from collections import Counter
        nums, k = inputs["nums"], inputs["k"]
        return [x for x, _ in Counter(nums).most_common(k)]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(3, 20)
            nums = [rng.randint(1, 8) for _ in range(n)]
            from collections import Counter
            unique = len(Counter(nums))
            k = rng.randint(1, max(1, unique))
            tests.append({"nums": nums, "k": k})
        return tests
