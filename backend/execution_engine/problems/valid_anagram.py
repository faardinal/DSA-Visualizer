from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator

class ValidAnagramPlugin(ProblemPlugin):
    problem_id = "valid-anagram"
    leetcode_number = 242
    slug = "valid-anagram"
    title = "Valid Anagram"
    method_name = "isAnagram"
    difficulty = "Easy"
    pattern = "Hashing"
    topics = ["Hash Table", "String", "Sorting"]
    parameters = ["s: str", "t: str"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given two strings s and t, return true if t is an anagram of s, and false otherwise."

    def get_test_cases(self):
        return [
            TestCase({"s": "anagram", "t": "nagaram"}, True, "Example 1"),
            TestCase({"s": "rat", "t": "car"}, False, "Example 2"),
            TestCase({"s": "", "t": ""}, True, "Empty strings", is_hidden=True),
            TestCase({"s": "a", "t": "a"}, True, "Single char", is_hidden=True),
            TestCase({"s": "ab", "t": "a"}, False, "Different lengths", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import Counter
        return Counter(inputs["s"]) == Counter(inputs["t"])

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for i in range(count):
            chars = list(string.ascii_lowercase[:10])
            base = [rng.choice(chars) for _ in range(rng.randint(1, 15))]
            if i % 2 == 0:
                shuffled = base[:]
                rng.shuffle(shuffled)
                tests.append({"s": "".join(base), "t": "".join(shuffled)})
            else:
                other = [rng.choice(chars) for _ in range(rng.randint(1, 15))]
                tests.append({"s": "".join(base), "t": "".join(other)})
        return tests
