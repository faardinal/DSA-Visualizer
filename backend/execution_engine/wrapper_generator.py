"""
Template-based wrapper code generator for the execution engine.

Each DSA pattern has a reusable template. The generator selects the
appropriate template, injects the user's Solution code, helper classes,
and test execution code with result markers.
"""

import json
from typing import Optional

from .parser import ParsedSolution, MethodInfo
from .plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from .type_hints import TypeHint, is_node_type, is_collection_type
from .object_builder import (
    LIST_NODE_HELPERS, TREE_NODE_HELPERS, TRIE_NODE_HELPERS, GRAPH_HELPERS,
)


# LeetCode supplies these names to ordinary submissions. Keeping the prelude
# outside user code lets `List[int]` and common helpers work without imports.
COMMON_LEETCODE_PRELUDE = """from typing import Any, Dict, List, Optional, Set, Tuple, Union
from collections import Counter, defaultdict, deque, OrderedDict
from functools import lru_cache
from bisect import bisect_left, bisect_right
import heapq
import math
"""


# ---------------------------------------------------------------------------
# Template strings
# ---------------------------------------------------------------------------

# Standard template for problems with simple parameters (arrays, ints, strings)
GENERIC_TEMPLATE = """
{imports}

{helpers}

# === Solution code ===
{solution_code}

# === Test execution ===
def main():
{param_assignments}

    sol = Solution()
    result = sol.{method_name}({param_names})

    # Serialize result for comparison
    _result = repr(result)
    print("__RESULT__:")
    print(_result)

main()
"""

# Template for linked list problems
LINKED_LIST_TEMPLATE = """
{imports}

{helpers}

# === Solution code ===
{solution_code}

# === Test execution ===
def main():
{param_assignments}

    # Serialize input for before-state capture
    _input_before = []
{before_captures}

    sol = Solution()
    result = sol.{method_name}({param_names})

    # Serialize result
    _serialized = _serialize_result(result)
    print("__RESULT__:")
    print(repr(_serialized))
    print("__INPUT_BEFORE__:")
    print(repr(_input_before))

def _serialize_result(r):
    if hasattr(r, 'val'):
        from collections import deque
        items = []
        current = r
        visited = set()
        while current is not None:
            nid = id(current)
            if nid in visited:
                break
            visited.add(nid)
            items.append(current.val)
            current = current.next
            if len(items) > 5000:
                break
        return items
    if hasattr(r, 'left'):
        result = []
        queue = deque([r])
        while queue:
            node = queue.popleft()
            if node is None:
                result.append(None)
                continue
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        while result and result[-1] is None:
            result.pop()
        return result
    return r

main()
"""

# Template for tree problems
TREE_TEMPLATE = LINKED_LIST_TEMPLATE  # Same structure, works for both

# Template for graph/matrix problems
GRAPH_TEMPLATE = """
{imports}

{helpers}

# === Solution code ===
{solution_code}

# === Test execution ===
def main():
{param_assignments}

    sol = Solution()
    result = sol.{method_name}({param_names})

    print("__RESULT__:")
    print(repr(result))

main()
"""

# Template for in-place mutation problems
IN_PLACE_TEMPLATE = """
{imports}

import copy

{helpers}

# === Solution code ===
{solution_code}

# === Test execution ===
def main():
{param_assignments}

    # Capture state before mutation
    _state_before = {}
{before_captures}

    sol = Solution()
    result = sol.{method_name}({param_names})

    # Capture state after mutation
    _state_after = {}
{after_captures}

    # For in-place problems, the result is the mutated object
    _output = result
    print("__RESULT__:")
    print(repr(_output))
    print("__INPUT_BEFORE__:")
    print(repr(_state_before))
    print("__INPUT_AFTER__:")
    print(repr(_state_after))

main()
"""


# ---------------------------------------------------------------------------
# Wrapper generator
# ---------------------------------------------------------------------------

def generate_wrapper(
    solution_code: str,
    parsed: ParsedSolution,
    plugin: Optional[ProblemPlugin],
    test_case: TestCase,
    method: MethodInfo,
) -> str:
    """
    Generate a complete Python wrapper that executes the user's solution
    against a single test case.

    Args:
        solution_code: The user's Python source code (Solution class).
        parsed: Parsed AST information about the Solution class.
        plugin: The registered ProblemPlugin (or None for unknown problems).
        test_case: The test case to run.
        method: The specific MethodInfo to execute.

    Returns:
        Complete Python source string ready for exec().
    """
    # Use plugin's custom template if provided
    if plugin and plugin.get_wrapper_template():
        custom_tpl = plugin.get_wrapper_template()
        return _fill_custom_template(custom_tpl, solution_code, test_case, method)

    # Auto-detect template from parameter types
    template = _select_template(parsed, method, plugin, test_case)

    # Build parameter assignments and names
    param_assignments = []
    param_names = []
    before_captures = []
    after_captures = []

    for param in method.params:
        value = test_case.inputs.get(param.name)
        if value is None and param.name not in test_case.inputs:
            continue

        # Determine how to assign the parameter
        value_repr = _value_to_python_repr(value, param)
        param_assignments.append(f"    {param.name} = {value_repr}")
        param_names.append(param.name)

        # Add before/after captures for mutable types
        if isinstance(value, list) and not _is_primitive_param(param):
            safe_copy = "copy.deepcopy(" + param.name + ")"
            before_captures.append(f"    _input_before.append({safe_copy})")
            after_captures.append(f"    _state_after['{param.name}'] = {safe_copy}")

    input_repr = test_case.input_repr()

    # Select helpers based on types needed
    imports_str = COMMON_LEETCODE_PRELUDE
    helpers_str = ""
    if _needs_linked_list(parsed, method):
        helpers_str += LIST_NODE_HELPERS
    if _needs_tree(parsed, method):
        helpers_str += TREE_NODE_HELPERS
    if any(param.annotation and "TrieNode" in param.annotation.raw for param in method.params):
        helpers_str += TRIE_NODE_HELPERS
    if _needs_graph(parsed, method):
        helpers_str += GRAPH_HELPERS

    # IMPORTANT: We use str.replace() instead of str.format() because the
    # user's solution_code can contain literal { } characters (dict/set/f-string
    # syntax), which would break str.format().
    replacements = {
        "{imports}": imports_str,
        "{helpers}": helpers_str,
        "{solution_code}": solution_code,
        "{method_name}": method.name,
        "{param_assignments}": "\n".join(param_assignments) if param_assignments else "    pass",
        "{param_names}": ", ".join(param_names),
        "{input_repr}": input_repr,
        "{before_captures}": "\n".join(before_captures) if before_captures else "    pass",
        "{after_captures}": "\n".join(after_captures) if after_captures else "    pass",
    }
    wrapper = template
    for placeholder, value in replacements.items():
        wrapper = wrapper.replace(placeholder, value)

    return wrapper


def _fill_custom_template(
    template: WrapperTemplate,
    solution_code: str,
    test_case: TestCase,
    method: MethodInfo,
) -> str:
    """Fill a plugin's custom template with test case data."""
    # Built-in placeholders (helpers/imports) are filled from the WrapperTemplate
    replacements = {
        "solution_code": solution_code,
        "helpers": template.helpers_str or "",
        "imports": COMMON_LEETCODE_PRELUDE + (template.imports_str or ""),
    }

    # Parameter value replacements
    for param in method.params:
        value = test_case.inputs.get(param.name)
        value_repr = _value_to_python_repr(value, param)
        replacements[param.name] = value_repr

    # Replace {placeholders} in template
    result = template.template_str
    for key, val in replacements.items():
        result = result.replace("{" + key + "}", val)

    return result


def _select_template(parsed, method, plugin, test_case) -> str:
    """Select the appropriate wrapper template based on the problem type."""
    # Check for in-place pattern (plugin metadata or method name hints)
    if plugin:
        pattern = plugin.pattern.lower()
        if "in-place" in pattern or "in place" in pattern:
            return IN_PLACE_TEMPLATE
        if "linked" in pattern or "linked list" in pattern:
            return LINKED_LIST_TEMPLATE
        if "tree" in pattern or "bst" in pattern:
            return TREE_TEMPLATE
        if "graph" in pattern:
            return GRAPH_TEMPLATE

    # Auto-detect from parameter types
    if _needs_linked_list(parsed, method):
        return LINKED_LIST_TEMPLATE
    if _needs_tree(parsed, method):
        return TREE_TEMPLATE

    # Check if any param is a mutable list (potential in-place)
    if _is_in_place_problem(parsed, method, test_case):
        return IN_PLACE_TEMPLATE

    return GENERIC_TEMPLATE


def _needs_linked_list(parsed: ParsedSolution, method: MethodInfo) -> bool:
    """Check if any parameter or return type involves ListNode."""
    for param in method.params:
        if param.annotation and is_node_type(param.annotation):
            if "ListNode" in param.annotation.raw or "Node" in param.annotation.raw:
                return True
    if method.return_annotation and "ListNode" in method.return_annotation.raw:
        return True
    return False


def _needs_tree(parsed: ParsedSolution, method: MethodInfo) -> bool:
    """Check if any parameter or return type involves TreeNode."""
    for param in method.params:
        if param.annotation and "TreeNode" in param.annotation.raw:
            return True
    if method.return_annotation and "TreeNode" in method.return_annotation.raw:
        return True
    return False


def _needs_graph(parsed: ParsedSolution, method: MethodInfo) -> bool:
    """Check if any parameter involves graph-like types."""
    for param in method.params:
        if param.annotation and "graph" in param.annotation.raw.lower():
            return True
    return False


def _is_in_place_problem(parsed, method, test_case) -> bool:
    """Heuristic: detect in-place problems by return type + mutable params."""
    # If return type is None and there's a mutable list param, likely in-place
    if method.return_annotation_str in ("None", "", "NoneType"):
        for param in method.params:
            ann = param.annotation
            if ann and is_collection_type(ann):
                return True
    # If return type is None and method name suggests mutation
    mutation_names = {"merge", "sort", "rotate", "move", "set", "reverse",
                      "modify", "update", "remove", "replace", "swap",
                      "flatten", "sortcolors", "nextpermutation"}
    if method.name.lower() in mutation_names:
        return True
    return False


def _is_primitive_param(param) -> bool:
    """Check if a parameter is a primitive type."""
    if not param.annotation:
        return True
    ann = param.annotation
    return ann.base in ("int", "float", "bool", "str", "None", "NoneType")


def _value_to_python_repr(value, param=None) -> str:
    """Convert a JSON-like value to a Python literal representation."""
    if param and param.annotation_str:
        raw_type = param.annotation_str.replace(" ", "")
        raw_repr = _value_to_python_repr(value)
        if "ListNode" in raw_type:
            return f"build_linked_list({raw_repr})"
        if "TreeNode" in raw_type:
            return f"build_binary_tree({raw_repr})"
        if "TrieNode" in raw_type:
            return f"build_trie({raw_repr})"
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, list):
        items = ", ".join(_value_to_python_repr(item) for item in value)
        return f"[{items}]"
    if isinstance(value, dict):
        items = ", ".join(
            f"{_value_to_python_repr(k)}: {_value_to_python_repr(v)}"
            for k, v in value.items()
        )
        return f"{{{items}}}"
    if isinstance(value, tuple):
        items = ", ".join(_value_to_python_repr(item) for item in value)
        return f"({items})"
    return repr(value)
