from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator

class ContainsDuplicatePlugin(ProblemPlugin):
    problem_id = "contains-duplicate"
    leetcode_number = 217
    slug = "contains-duplicate"
    title = "Contains Duplicate"
    method_name = "containsDuplicate"
    difficulty = "Easy"
    pattern = "Array"
    topics = ["Array", "Hash Table", "Sorting"]
    parameters = ["nums: List[int]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct."

    def get_test_cases(self):
        return [
            TestCase({"nums": [1,2,3,1]}, True, "Example 1"),
            TestCase({"nums": [1,2,3,4]}, False, "Example 2"),
            TestCase({"nums": [1,1,1,3,3,4,3,2,4,2]}, True, "Example 3"),
            TestCase({"nums": []}, False, "Empty array", is_hidden=True),
            TestCase({"nums": [1]}, False, "Single element", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        return len(inputs["nums"]) != len(set(inputs["nums"]))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            if i % 2 == 0:
                n = rng.randint(2, 20)
                nums = [rng.randint(1, 10) for _ in range(n)]
            else:
                n = rng.randint(2, 20)
                nums = list(range(n))
                rng.shuffle(nums)
            tests.append({"nums": nums})
        return tests
