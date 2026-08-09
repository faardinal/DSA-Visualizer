from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import Validator, ValidationResult

class GroupAnagramsPlugin(ProblemPlugin):
    problem_id = "group-anagrams"
    leetcode_number = 49
    slug = "group-anagrams"
    title = "Group Anagrams"
    method_name = "groupAnagrams"
    difficulty = "Medium"
    pattern = "Hashing"
    topics = ["Array", "Hash Table", "String", "Sorting"]
    parameters = ["strs: List[str]"]
    return_type = "List[List[str]]"
    hidden_test_count = 4
    description = "Given an array of strings strs, group the anagrams together. You can return the answer in any order."

    def get_test_cases(self):
        return [
            TestCase({"strs": ["eat","tea","tan","ate","nat","bat"]},
                     [["bat"],["nat","tan"],["ate","eat","tea"]], "Example 1"),
            TestCase({"strs": [""]}, [[""]], "Example 2"),
            TestCase({"strs": ["a"]}, [["a"]], "Example 3"),
            TestCase({"strs": ["ab","ba","abc","bca","cab"]},
                     [["ab","ba"],["abc","bca","cab"]], "Hidden: multiple groups", is_hidden=True),
        ]

    def get_validator(self): return GroupAnagramsValidator()

    @staticmethod
    def oracle(inputs):
        from collections import defaultdict
        groups = defaultdict(list)
        for s in inputs["strs"]:
            groups[tuple(sorted(s))].append(s)
        return sorted(sorted(g) for g in groups.values())

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for _ in range(count):
            chars = list(string.ascii_lowercase[:8])
            strs = []
            for _ in range(rng.randint(3, 12)):
                word = [rng.choice(chars) for _ in range(rng.randint(1, 5))]
                strs.append("".join(word))
            tests.append({"strs": strs})
        return tests


class GroupAnagramsValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        try:
            a = sorted(sorted(g) for g in actual)
            e = sorted(sorted(g) for g in expected)
            passed = a == e
        except Exception:
            passed = False
            a, e = actual, expected
        return ValidationResult(passed, repr(e), repr(a),
                                "" if passed else f"Groups don't match")
