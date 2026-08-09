from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator

class ProductExceptSelfPlugin(ProblemPlugin):
    problem_id = "product-of-array-except-self"
    leetcode_number = 238
    slug = "product-of-array-except-self"
    title = "Product of Array Except Self"
    method_name = "productExceptSelf"
    difficulty = "Medium"
    pattern = "Array"
    topics = ["Array", "Prefix Sum"]
    parameters = ["nums: List[int]"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = "Given an integer array nums, return an array answer such that answer[i] is equal to the product of all elements of nums except nums[i]."

    def get_test_cases(self):
        return [
            TestCase({"nums": [1,2,3,4]}, [24,12,8,6], "Example 1"),
            TestCase({"nums": [-1,1,0,-3,3]}, [0,0,9,0,0], "Example 2"),
            TestCase({"nums": [2,3]}, [3,2], "Two elements", is_hidden=True),
            TestCase({"nums": [1,0]}, [0,1], "With zero", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums = inputs["nums"]
        n = len(nums)
        result = [1] * n
        left = 1
        for i in range(n):
            result[i] = left
            left *= nums[i]
        right = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right
            right *= nums[i]
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            n = rng.randint(2, 15)
            if i % 3 == 0:
                nums = [rng.randint(-5, 5) for _ in range(n)]
            else:
                nums = [rng.randint(1, 10) for _ in range(n)]
            tests.append({"nums": nums})
        return tests
