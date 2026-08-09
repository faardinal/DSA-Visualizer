"""Encode and Decode Strings — LeetCode 271 (premium). Stateful design problem."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator

_WRAPPER = '''
{imports}

{helpers}

{solution_code}

def main():
    codec = Codec()
    strs = {strs}
    encoded = codec.encode(strs)
    decoded = codec.decode(encoded)
    print("__RESULT__:")
    print(repr(decoded))

main()
'''

class EncodeDecodeStringsPlugin(ProblemPlugin):
    problem_id = "encode-and-decode-strings"
    leetcode_number = 271
    slug = "encode-and-decode-strings"
    title = "Encode and Decode Strings"
    method_name = "encode"
    difficulty = "Medium"
    pattern = "Hashing"
    topics = ["Array", "String", "Design"]
    parameters = ["strs: List[str]"]
    return_type = "str"
    hidden_test_count = 3
    description = (
        "Design an algorithm to encode a list of strings to a single string. "
        "The encoded string is then sent over the network and decoded back to the original list."
    )

    def get_test_cases(self):
        return [
            TestCase({"strs": ["neet","code","love","you"]},
                     ["neet","code","love","you"], "Example 1"),
            TestCase({"strs": ["we","say",":","yes"]},
                     ["we","say",":","yes"], "Example 2"),
            TestCase({"strs": [""]}, [""], "Empty string element", is_hidden=True),
            TestCase({"strs": ["a","b","c"]}, ["a","b","c"], "Single chars", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_WRAPPER)

    @staticmethod
    def oracle(inputs):
        return inputs["strs"]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for _ in range(count):
            strs = ["".join(rng.choices(string.printable[:50], k=rng.randint(0,8)))
                    for _ in range(rng.randint(1,6))]
            tests.append({"strs": strs})
        return tests
