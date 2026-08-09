"""Linked List pattern problems.

All problems that take or return ListNode chains. The wrapper_generator
auto-injects LIST_NODE_HELPERS when it detects ListNode in parameter types,
so user solutions can use ListNode directly just like on LeetCode.
"""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult
from backend.execution_engine.object_builder import (
    build_linked_list, serialize_linked_list, LIST_NODE_HELPERS
)

# ── shared custom wrapper template ────────────────────────────────────────
# Used for "returns ListNode" problems. Converts list→ListNode, runs
# Solution, serialises output back to list for comparison.
_LL_RETURN_WRAPPER = '''{imports}

{helpers}

{solution_code}

def main():
    sol = Solution()
    result = sol.{method}({call_args})
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
'''

_LL_INPLACE_WRAPPER = '''{imports}

{helpers}

{solution_code}

def main():
    sol = Solution()
    sol.{method}({call_args})
    print("__RESULT__:")
    print(repr(serialize_linked_list({first_arg})))

main()
'''


def _make_ll_return(method, params):
    """Build a custom WrapperTemplate for 'returns ListNode' problems."""
    assigns = "\n".join(
        f"    {name} = build_linked_list({repr(None)})"  # placeholder; runtime fills
        for name, _tp in params
    )
    # Build the real template with {paramN} placeholders filled at test time
    call = ", ".join(n for n, _ in params)
    body = ''.join(
        f"    {name} = build_linked_list({{{name}}})\n"
        for name, tp in params if tp == "list"
    ) + ''.join(
        f"    {name} = {{{name}}}\n"
        for name, tp in params if tp != "list"
    )
    tpl = (
        "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
        "def main():\n"
        + body +
        f"    sol = Solution()\n"
        f"    result = sol.{method}({call})\n"
        "    print('__RESULT__:')\n"
        "    print(repr(serialize_linked_list(result)))\n\n"
        "main()\n"
    )
    return WrapperTemplate(template_str=tpl, helpers_str=LIST_NODE_HELPERS)


# ── Validator for linked-list output (compare as arrays) ─────────────────
class LinkedListValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        passed = actual == expected
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected list {expected!r}, got {actual!r}")


# ═══════════════════════════════════════════════════════════════════════════
# LC 206 — Reverse Linked List  (already in reverse_linked_list.py — skip)
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# LC 21 — Merge Two Sorted Lists
# ═══════════════════════════════════════════════════════════════════════════
_MERGE_TPL = """{imports}

{helpers}

{solution_code}

def main():
    list1 = build_linked_list({list1})
    list2 = build_linked_list({list2})
    sol = Solution()
    result = sol.mergeTwoLists(list1, list2)
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""

class MergeTwoSortedListsPlugin(ProblemPlugin):
    problem_id = "merge-two-sorted-lists"
    leetcode_number = 21
    title = "Merge Two Sorted Lists"
    slug = "merge-two-sorted-lists"
    method_name = "mergeTwoLists"
    difficulty = "Easy"
    pattern = "Linked List"
    topics = ["Linked List", "Recursion"]
    parameters = ["list1: Optional[ListNode]", "list2: Optional[ListNode]"]
    return_type = "Optional[ListNode]"
    hidden_test_count = 4
    description = "Merge two sorted linked lists and return the head of the merged sorted list."

    def get_test_cases(self):
        return [
            TestCase({"list1": [1,2,4], "list2": [1,3,4]}, [1,1,2,3,4,4], "Example 1"),
            TestCase({"list1": [], "list2": []}, [], "Example 2"),
            TestCase({"list1": [], "list2": [0]}, [0], "Example 3"),
            TestCase({"list1": [1], "list2": [2]}, [1,2], "Two singles", is_hidden=True),
            TestCase({"list1": [1,3,5], "list2": [2,4,6]}, [1,2,3,4,5,6], "Interleaved", is_hidden=True),
        ]

    def get_validator(self): return LinkedListValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_MERGE_TPL, helpers_str=LIST_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        a = sorted(inputs["list1"] + inputs["list2"])
        return a

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n1 = rng.randint(0, 8); n2 = rng.randint(0, 8)
            l1 = sorted(rng.randint(-10, 10) for _ in range(n1))
            l2 = sorted(rng.randint(-10, 10) for _ in range(n2))
            tests.append({"list1": l1, "list2": l2})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 141 — Linked List Cycle
# ═══════════════════════════════════════════════════════════════════════════
_CYCLE_TPL = """{imports}

{helpers}

{solution_code}

def main():
    nodes_data = {nodes}
    pos = {pos}
    # Build list with optional cycle
    if not nodes_data:
        head = None
    else:
        nodes = [ListNode(v) for v in nodes_data]
        for i in range(len(nodes)-1):
            nodes[i].next = nodes[i+1]
        if pos >= 0 and pos < len(nodes):
            nodes[-1].next = nodes[pos]
        head = nodes[0]
    sol = Solution()
    result = sol.hasCycle(head)
    print("__RESULT__:")
    print(repr(result))

main()
"""

class LinkedListCyclePlugin(ProblemPlugin):
    problem_id = "linked-list-cycle"
    leetcode_number = 141
    title = "Linked List Cycle"
    slug = "linked-list-cycle"
    method_name = "hasCycle"
    difficulty = "Easy"
    pattern = "Linked List"
    topics = ["Hash Table", "Linked List", "Two Pointers"]
    parameters = ["head: Optional[ListNode]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given head of a linked list, determine if the linked list has a cycle in it."

    def get_test_cases(self):
        return [
            TestCase({"nodes": [3,2,0,-4], "pos": 1}, True, "Example 1: cycle at index 1"),
            TestCase({"nodes": [1,2], "pos": 0}, True, "Example 2: cycle at index 0"),
            TestCase({"nodes": [1], "pos": -1}, False, "Example 3: no cycle"),
            TestCase({"nodes": [], "pos": -1}, False, "Empty list", is_hidden=True),
            TestCase({"nodes": [1,2,3,4,5], "pos": -1}, False, "No cycle, 5 nodes", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_CYCLE_TPL, helpers_str=LIST_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        return inputs["pos"] >= 0

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            n = rng.randint(1, 8)
            nodes = [rng.randint(-10, 10) for _ in range(n)]
            pos = rng.randint(0, n-1) if i % 2 == 0 else -1
            tests.append({"nodes": nodes, "pos": pos})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 143 — Reorder List
# ═══════════════════════════════════════════════════════════════════════════
_REORDER_TPL = """{imports}

{helpers}

{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    sol.reorderList(head)
    print("__RESULT__:")
    print(repr(serialize_linked_list(head)))

main()
"""

class ReorderListPlugin(ProblemPlugin):
    problem_id = "reorder-list"
    leetcode_number = 143
    title = "Reorder List"
    slug = "reorder-list"
    method_name = "reorderList"
    difficulty = "Medium"
    pattern = "Linked List"
    topics = ["Linked List", "Two Pointers", "Stack", "Recursion"]
    parameters = ["head: Optional[ListNode]"]
    return_type = "None"
    hidden_test_count = 4
    description = (
        "You are given the head of a singly linked-list: L0→L1→…→Ln-1→Ln. "
        "Reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…"
    )

    def get_test_cases(self):
        return [
            TestCase({"head": [1,2,3,4]}, [1,4,2,3], "Example 1"),
            TestCase({"head": [1,2,3,4,5]}, [1,5,2,4,3], "Example 2"),
            TestCase({"head": [1]}, [1], "Single node", is_hidden=True),
            TestCase({"head": [1,2]}, [1,2], "Two nodes", is_hidden=True),
        ]

    def get_validator(self): return LinkedListValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_REORDER_TPL, helpers_str=LIST_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        vals = inputs["head"]
        if not vals: return []
        result = []
        l, r = 0, len(vals)-1
        while l <= r:
            result.append(vals[l]); l += 1
            if l <= r:
                result.append(vals[r]); r -= 1
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 10)
            tests.append({"head": list(range(1, n+1))})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 19 — Remove Nth Node From End of List
# ═══════════════════════════════════════════════════════════════════════════
_REMOVE_NTH_TPL = """{imports}

{helpers}

{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.removeNthFromEnd(head, {n})
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""

class RemoveNthFromEndPlugin(ProblemPlugin):
    problem_id = "remove-nth-node-from-end-of-list"
    leetcode_number = 19
    title = "Remove Nth Node From End of List"
    slug = "remove-nth-node-from-end-of-list"
    method_name = "removeNthFromEnd"
    difficulty = "Medium"
    pattern = "Linked List"
    topics = ["Linked List", "Two Pointers"]
    parameters = ["head: Optional[ListNode]", "n: int"]
    return_type = "Optional[ListNode]"
    hidden_test_count = 4
    description = "Given the head of a linked list, remove the nth node from the end of the list and return its head."

    def get_test_cases(self):
        return [
            TestCase({"head": [1,2,3,4,5], "n": 2}, [1,2,3,5], "Example 1"),
            TestCase({"head": [1], "n": 1}, [], "Example 2"),
            TestCase({"head": [1,2], "n": 1}, [1], "Example 3"),
            TestCase({"head": [1,2,3], "n": 3}, [2,3], "Remove head", is_hidden=True),
        ]

    def get_validator(self): return LinkedListValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_REMOVE_NTH_TPL, helpers_str=LIST_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        vals = list(inputs["head"])
        n = inputs["n"]
        idx = len(vals) - n
        del vals[idx]
        return vals

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            length = rng.randint(1, 10)
            vals = [rng.randint(1, 20) for _ in range(length)]
            n = rng.randint(1, length)
            tests.append({"head": vals, "n": n})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 138 — Copy List with Random Pointer
# ═══════════════════════════════════════════════════════════════════════════
_COPY_RANDOM_TPL = """{imports}

{helpers}

# Node with random pointer
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random

{solution_code}

def main():
    pairs = {pairs}
    if not pairs:
        head = None
    else:
        nodes = [Node(p[0]) for p in pairs]
        for i in range(len(nodes)-1):
            nodes[i].next = nodes[i+1]
        for i, p in enumerate(pairs):
            if p[1] is not None:
                nodes[i].random = nodes[p[1]]
        head = nodes[0]
    sol = Solution()
    result = sol.copyRandomList(head)
    # Serialize as [[val, random_idx or None], ...]
    out = []
    if result:
        node_list = []
        cur = result
        while cur:
            node_list.append(cur)
            cur = cur.next
        idx_map = {{id(n): i for i, n in enumerate(node_list)}}
        for n in node_list:
            out.append([n.val, idx_map.get(id(n.random)) if n.random else None])
    print("__RESULT__:")
    print(repr(out))

main()
"""

class CopyListWithRandomPointerPlugin(ProblemPlugin):
    problem_id = "copy-list-with-random-pointer"
    leetcode_number = 138
    title = "Copy List with Random Pointer"
    slug = "copy-list-with-random-pointer"
    method_name = "copyRandomList"
    difficulty = "Medium"
    pattern = "Linked List"
    topics = ["Hash Table", "Linked List"]
    parameters = ["head: Optional[Node]"]
    return_type = "Optional[Node]"
    hidden_test_count = 3
    description = (
        "A linked list of length n is given such that each node contains an additional random pointer. "
        "Construct a deep copy of the list."
    )

    def get_test_cases(self):
        return [
            TestCase({"pairs": [[7,None],[13,0],[11,4],[10,2],[1,0]]},
                     [[7,None],[13,0],[11,4],[10,2],[1,0]], "Example 1"),
            TestCase({"pairs": [[1,1],[2,1]]}, [[1,1],[2,1]], "Example 2"),
            TestCase({"pairs": []}, [], "Empty list", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_COPY_RANDOM_TPL)

    @staticmethod
    def oracle(inputs):
        return inputs["pairs"]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 6)
            pairs = []
            for _ in range(n):
                rand_idx = rng.randint(0, n-1) if rng.random() > 0.3 else None
                pairs.append([rng.randint(1, 20), rand_idx])
            tests.append({"pairs": pairs})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 2 — Add Two Numbers
# ═══════════════════════════════════════════════════════════════════════════
_ADD_TWO_TPL = """{imports}

{helpers}

{solution_code}

def main():
    l1 = build_linked_list({l1})
    l2 = build_linked_list({l2})
    sol = Solution()
    result = sol.addTwoNumbers(l1, l2)
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""

class AddTwoNumbersPlugin(ProblemPlugin):
    problem_id = "add-two-numbers"
    leetcode_number = 2
    title = "Add Two Numbers"
    slug = "add-two-numbers"
    method_name = "addTwoNumbers"
    difficulty = "Medium"
    pattern = "Linked List"
    topics = ["Linked List", "Math", "Recursion"]
    parameters = ["l1: Optional[ListNode]", "l2: Optional[ListNode]"]
    return_type = "Optional[ListNode]"
    hidden_test_count = 4
    description = (
        "You are given two non-empty linked lists representing two non-negative integers. "
        "The digits are stored in reverse order. Return the sum as a linked list."
    )

    def get_test_cases(self):
        return [
            TestCase({"l1": [2,4,3], "l2": [5,6,4]}, [7,0,8], "Example 1: 342+465=807"),
            TestCase({"l1": [0], "l2": [0]}, [0], "Example 2"),
            TestCase({"l1": [9,9,9,9,9,9,9], "l2": [9,9,9,9]}, [8,9,9,9,0,0,0,1], "Example 3"),
            TestCase({"l1": [1], "l2": [9,9]}, [0,0,1], "Carry across lengths", is_hidden=True),
        ]

    def get_validator(self): return LinkedListValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_ADD_TWO_TPL, helpers_str=LIST_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def ll_to_int(digits):
            return int("".join(str(d) for d in reversed(digits)) or "0")
        s = ll_to_int(inputs["l1"]) + ll_to_int(inputs["l2"])
        result = []
        if s == 0: return [0]
        while s:
            result.append(s % 10)
            s //= 10
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            a = rng.randint(0, 9999)
            b = rng.randint(0, 9999)
            def to_rev_digits(n):
                if n == 0: return [0]
                d = []
                while n: d.append(n%10); n//=10
                return d
            tests.append({"l1": to_rev_digits(a), "l2": to_rev_digits(b)})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 287 — Find the Duplicate Number
# ═══════════════════════════════════════════════════════════════════════════
class FindDuplicatePlugin(ProblemPlugin):
    problem_id = "find-the-duplicate-number"
    leetcode_number = 287
    title = "Find the Duplicate Number"
    slug = "find-the-duplicate-number"
    method_name = "findDuplicate"
    difficulty = "Medium"
    pattern = "Linked List"
    topics = ["Array", "Two Pointers", "Binary Search", "Bit Manipulation"]
    parameters = ["nums: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Given an array of integers nums containing n+1 integers where each integer is in [1,n], "
        "return the one repeated number."
    )

    def get_test_cases(self):
        return [
            TestCase({"nums": [1,3,4,2,2]}, 2, "Example 1"),
            TestCase({"nums": [3,1,3,4,2]}, 3, "Example 2"),
            TestCase({"nums": [1,1]}, 1, "Two elements"),
            TestCase({"nums": [2,2,2,2,2]}, 2, "All same", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        seen = set()
        for n in inputs["nums"]:
            if n in seen: return n
            seen.add(n)
        return -1

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 10)
            base = list(range(1, n+1))
            dup = rng.randint(1, n)
            base.append(dup)
            rng.shuffle(base)
            tests.append({"nums": base})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 146 — LRU Cache  (stateful design)
# ═══════════════════════════════════════════════════════════════════════════
_LRU_TPL = """{imports}

{helpers}

{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    cap  = args[0][0]
    obj  = LRUCache(cap)
    for op, arg in zip(ops[1:], args[1:]):
        if op == "put":
            obj.put(arg[0], arg[1])
            out.append(None)
        elif op == "get":
            out.append(obj.get(arg[0]))
    print("__RESULT__:")
    print(repr(out))

main()
"""

class LRUCachePlugin(ProblemPlugin):
    problem_id = "lru-cache"
    leetcode_number = 146
    title = "LRU Cache"
    slug = "lru-cache"
    method_name = "get"
    difficulty = "Medium"
    pattern = "Linked List"
    topics = ["Hash Table", "Linked List", "Design", "Doubly-Linked List"]
    parameters = ["key: int"]
    return_type = "int"
    hidden_test_count = 3
    stateful = True
    description = (
        "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache."
    )

    def get_test_cases(self):
        return [
            TestCase(
                {"ops": ["LRUCache","put","put","get","put","get","put","get","get","get"],
                 "args": [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]},
                [None,None,None,1,None,-1,None,-1,3,4],
                "Example 1"
            ),
            TestCase(
                {"ops": ["LRUCache","put","get"],
                 "args": [[1],[2,1],[2]]},
                [None,None,1],
                "Simple get after put", is_hidden=True
            ),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_LRU_TPL)

    @staticmethod
    def oracle(inputs):
        from collections import OrderedDict
        ops, args = inputs["ops"], inputs["args"]
        cap = args[0][0]
        cache = OrderedDict()
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "put":
                k, v = arg[0], arg[1]
                if k in cache: del cache[k]
                cache[k] = v
                if len(cache) > cap:
                    cache.popitem(last=False)
                out.append(None)
            elif op == "get":
                k = arg[0]
                if k not in cache:
                    out.append(-1)
                else:
                    cache.move_to_end(k)
                    out.append(cache[k])
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            cap = rng.randint(1, 4)
            ops = ["LRUCache"]; args = [[cap]]
            for _ in range(rng.randint(5, 12)):
                if rng.random() < 0.6:
                    k, v = rng.randint(1, 6), rng.randint(1, 20)
                    ops.append("put"); args.append([k, v])
                else:
                    k = rng.randint(1, 6)
                    ops.append("get"); args.append([k])
            tests.append({"ops": ops, "args": args})
        return tests
