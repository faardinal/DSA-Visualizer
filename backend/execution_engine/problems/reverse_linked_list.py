"""
Reverse Linked List problem plugin.
Pattern: Linked List
Difficulty: Easy
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
    WrapperTemplate,
)
from backend.execution_engine.object_builder import (
    LIST_NODE_HELPERS,
)


class ReverseLinkedListPlugin(ProblemPlugin):
    problem_id = "reverse-linked-list"
    leetcode_number = 206
    slug = "reverse-linked-list"
    title = "Reverse Linked List"
    method_name = "reverseList"
    difficulty = "Easy"
    pattern = "Linked List"
    topics = ["Linked List", "Recursion"]
    parameters = ["head: Optional[ListNode]"]
    return_type = "Optional[ListNode]"
    serialization = "linked_list"
    hidden_test_count = 2
    description = (
        "Given the head of a singly linked list, reverse the list "
        "and return the reversed list."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={"head": [1, 2, 3, 4, 5]},
                expected=[5, 4, 3, 2, 1],
                description="Example 1",
                is_hidden=False,
            ),
            TestCase(
                inputs={"head": [1, 2]},
                expected=[2, 1],
                description="Example 2",
                is_hidden=False,
            ),
            TestCase(
                inputs={"head": []},
                expected=[],
                description="Empty list",
                is_hidden=False,
            ),
            TestCase(
                inputs={"head": [1]},
                expected=[1],
                description="Hidden: single node",
                is_hidden=True,
            ),
            TestCase(
                inputs={"head": list(range(1, 21))},
                expected=list(range(20, 0, -1)),
                description="Hidden: 20 nodes",
                is_hidden=True,
            ),
        ]

    def get_validator(self):
        return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(
            template_str=LINKED_LIST_TEMPLATE,
            helpers_str=LIST_NODE_HELPERS,
            imports_str="",
        )

    @staticmethod
    def oracle(inputs):
        return list(reversed(inputs["head"]))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        return [{"head": [rng.randint(-100, 100) for _ in range(rng.randint(0, 40))]} for _ in range(count)]


LINKED_LIST_TEMPLATE = """
{helpers}

# === Solution code ===
{solution_code}

# === Test execution ===
def main():
    head = build_linked_list({head})
    input_before = serialize_linked_list(head)

    sol = Solution()
    result = sol.reverseList(head)
    result_serialized = serialize_linked_list(result)

    print(f"__RESULT__:\\n{repr(result_serialized)}")
    print(f"__INPUT_BEFORE__:\\n{repr(input_before)}")

main()
"""


class EqualityValidator(Validator):
    """Simple equality validator."""

    def validate(self, actual, expected):
        actual_repr = repr(actual)
        expected_repr = repr(expected)
        passed = actual == expected
        diff = "" if passed else f"Expected {expected_repr}, got {actual_repr}"
        return ValidationResult(passed, expected_repr, actual_repr, diff)
