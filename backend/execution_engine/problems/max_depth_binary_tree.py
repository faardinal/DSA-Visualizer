"""
Max Depth of Binary Tree problem plugin.
Pattern: Tree Traversal / Recursion
Difficulty: Easy
"""

from backend.execution_engine.plugin_base import (
    ProblemPlugin, TestCase, Validator, ValidationResult,
    WrapperTemplate,
)
from backend.execution_engine.object_builder import (
    TREE_NODE_HELPERS,
)


class MaxDepthBinaryTreePlugin(ProblemPlugin):
    problem_id = "max-depth-binary-tree"
    leetcode_number = 104
    slug = "maximum-depth-of-binary-tree"
    title = "Maximum Depth of Binary Tree"
    method_name = "maxDepth"
    difficulty = "Easy"
    pattern = "Tree Traversal"
    topics = ["Tree", "Depth-First Search", "Breadth-First Search"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "int"
    serialization = "tree_level_order"
    hidden_test_count = 2
    description = (
        "Given the root of a binary tree, return its maximum depth "
        "(the number of nodes along the longest path from root to leaf)."
    )

    def get_test_cases(self):
        return [
            TestCase(
                inputs={"root": [3, 9, 20, None, None, 15, 7]},
                expected=3,
                description="Example 1",
                is_hidden=False,
            ),
            TestCase(
                inputs={"root": [1, None, 2]},
                expected=2,
                description="Example 2",
                is_hidden=False,
            ),
            TestCase(
                inputs={"root": []},
                expected=0,
                description="Empty tree",
                is_hidden=False,
            ),
            TestCase(
                inputs={"root": [1]},
                expected=1,
                description="Hidden: single node",
                is_hidden=True,
            ),
            TestCase(
                inputs={
                    "root": [1, 2, 3, 4, None, None, 5, 6, None, None, None, None, 7]
                },
                expected=5,
                description="Hidden: unbalanced",
                is_hidden=True,
            ),
        ]

    def get_validator(self):
        return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(
            template_str=TREE_TEMPLATE,
            helpers_str=TREE_NODE_HELPERS,
            imports_str="",
        )

    @staticmethod
    def oracle(inputs):
        values = inputs["root"]
        if not values:
            return 0
        depth, queue = 0, [values[0]]
        index = 1
        while queue:
            level_size = len(queue)
            depth += 1
            for _ in range(level_size):
                node = queue.pop(0)
                if node is None:
                    continue
                for _ in range(2):
                    if index < len(values):
                        child = values[index]
                        index += 1
                        if child is not None:
                            queue.append(child)
        return depth

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            size = rng.randint(1, 31)
            values = [rng.randint(-100, 100)]
            for _ in range(1, size):
                values.append(None if rng.random() < 0.3 else rng.randint(-100, 100))
            tests.append({"root": values})
        return tests


TREE_TEMPLATE = """
{helpers}

# === Solution code ===
{solution_code}

# === Test execution ===
def main():
    root = build_binary_tree({root})
    input_before = serialize_binary_tree(root)

    sol = Solution()
    result = sol.maxDepth(root)

    print(f"__RESULT__:\\n{repr(result)}")
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
