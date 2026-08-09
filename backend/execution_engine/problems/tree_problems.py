"""Binary Tree / BST pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, Validator, ValidationResult, SortedListValidator
)
from backend.execution_engine.object_builder import TREE_NODE_HELPERS

# ── shared tree wrapper helpers ────────────────────────────────────────────
# Builds tree from level-order list, calls method, serialises result.

def _tree_tpl(method, in_params, out_type="tree"):
    """Generate a custom wrapper for tree-in / tree-or-primitive-out problems."""
    assigns = "\n".join(
        f"    {name} = build_binary_tree({{{name}}})" if tp == "tree" else f"    {name} = {{{name}}}"
        for name, tp in in_params
    )
    call_args = ", ".join(n for n, _ in in_params)
    if out_type == "tree":
        serialize = f"    print(repr(serialize_binary_tree(result)))"
    elif out_type == "list":
        serialize = f"    print(repr(result))"
    else:
        serialize = f"    print(repr(result))"
    return (
        "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
        "def main():\n"
        + assigns + "\n"
        f"    sol = Solution()\n"
        f"    result = sol.{method}({call_args})\n"
        "    print('__RESULT__:')\n"
        + serialize + "\n\n"
        "main()\n"
    )


# ═══════════════════════════════════════════════════════════════════════════
# LC 226 — Invert Binary Tree
# ═══════════════════════════════════════════════════════════════════════════
class InvertBinaryTreePlugin(ProblemPlugin):
    problem_id = "invert-binary-tree"
    leetcode_number = 226
    title = "Invert Binary Tree"
    slug = "invert-binary-tree"
    method_name = "invertTree"
    difficulty = "Easy"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BFS", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "Optional[TreeNode]"
    hidden_test_count = 4
    description = "Given the root of a binary tree, invert the tree, and return its root."

    def get_test_cases(self):
        return [
            TestCase({"root": [4,2,7,1,3,6,9]}, [4,7,2,9,6,3,1], "Example 1"),
            TestCase({"root": [2,1,3]}, [2,3,1], "Example 2"),
            TestCase({"root": []}, [], "Example 3: empty"),
            TestCase({"root": [1]}, [1], "Single node", is_hidden=True),
            TestCase({"root": [1,2]}, [1,None,2], "Left child only", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("invertTree", [("root","tree")], out_type="tree")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def inv(node_list):
            if not node_list: return []
            from collections import deque
            result = list(node_list)
            n = len(result)
            # level-order inversion
            q = deque([0])
            while q:
                i = q.popleft()
                l, r = 2*i+1, 2*i+2
                if l < n and r < n:
                    result[l], result[r] = result[r], result[l]
                if l < n and result[l] is not None: q.append(l)
                if r < n and result[r] is not None: q.append(r)
            # strip trailing None
            while result and result[-1] is None: result.pop()
            return result
        return inv(inputs["root"])

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(0, 10)
            vals = [rng.randint(1,50) if rng.random()>0.2 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0] = rng.randint(1,50)
            tests.append({"root": vals})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 543 — Diameter of Binary Tree
# ═══════════════════════════════════════════════════════════════════════════
class DiameterBinaryTreePlugin(ProblemPlugin):
    problem_id = "diameter-of-binary-tree"
    leetcode_number = 543
    title = "Diameter of Binary Tree"
    slug = "diameter-of-binary-tree"
    method_name = "diameterOfBinaryTree"
    difficulty = "Easy"
    pattern = "Trees"
    topics = ["Tree", "DFS", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given the root of a binary tree, return the length of the diameter of the tree."

    def get_test_cases(self):
        return [
            TestCase({"root": [1,2,3,4,5]}, 3, "Example 1"),
            TestCase({"root": [1,2]}, 1, "Example 2"),
            TestCase({"root": [1]}, 0, "Single node", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("diameterOfBinaryTree", [("root","tree")], out_type="int")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class _N:
                def __init__(self, v): self.val=v; self.left=self.right=None
            nodes = [None if v is None else _N(v) for v in items]
            q = deque([0]); i = 1
            while q and i < len(nodes):
                idx = q.popleft()
                if nodes[idx] is None: continue
                if i < len(nodes):
                    nodes[idx].left = nodes[i]; q.append(i); i+=1
                if i < len(nodes):
                    nodes[idx].right = nodes[i]; q.append(i); i+=1
            return nodes[0] if nodes else None
        root = build(inputs["root"])
        best = [0]
        def depth(node):
            if not node: return 0
            l, r = depth(node.left), depth(node.right)
            best[0] = max(best[0], l+r)
            return 1 + max(l, r)
        depth(root)
        return best[0]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 12)
            vals = [rng.randint(1,50) for _ in range(n)]
            # pad with Nones to make it a valid level-order tree
            tests.append({"root": vals})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 110 — Balanced Binary Tree
# ═══════════════════════════════════════════════════════════════════════════
class BalancedBinaryTreePlugin(ProblemPlugin):
    problem_id = "balanced-binary-tree"
    leetcode_number = 110
    title = "Balanced Binary Tree"
    slug = "balanced-binary-tree"
    method_name = "isBalanced"
    difficulty = "Easy"
    pattern = "Trees"
    topics = ["Tree", "DFS", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given a binary tree, determine if it is height-balanced (depth of two subtrees differs by ≤1)."

    def get_test_cases(self):
        return [
            TestCase({"root": [3,9,20,None,None,15,7]}, True, "Example 1"),
            TestCase({"root": [1,2,2,3,3,None,None,4,4]}, False, "Example 2"),
            TestCase({"root": []}, True, "Empty tree"),
            TestCase({"root": [1,2,3,4,5,6,None,8]}, True, "Balanced 8-node", is_hidden=True),
            TestCase({"root": [1,2,None,3,None,4]}, False, "Left-skewed", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("isBalanced", [("root","tree")], out_type="bool")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]
            q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        root=build(inputs["root"])
        def check(n):
            if not n: return 0
            l=check(n.left); r=check(n.right)
            if l<0 or r<0 or abs(l-r)>1: return -1
            return 1+max(l,r)
        return check(root)>=0

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(0, 15)
            vals = []
            for _ in range(n):
                vals.append(rng.randint(1,100) if rng.random()>0.15 else None)
            if vals and vals[0] is None: vals[0]=1
            tests.append({"root": vals})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 100 — Same Tree
# ═══════════════════════════════════════════════════════════════════════════
_SAME_TREE_TPL = (
    "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
    "def main():\n"
    "    p = build_binary_tree({p})\n"
    "    q = build_binary_tree({q})\n"
    "    sol = Solution()\n"
    "    result = sol.isSameTree(p, q)\n"
    "    print('__RESULT__:')\n"
    "    print(repr(result))\n\n"
    "main()\n"
)

class SameTreePlugin(ProblemPlugin):
    problem_id = "same-tree"
    leetcode_number = 100
    title = "Same Tree"
    slug = "same-tree"
    method_name = "isSameTree"
    difficulty = "Easy"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BFS", "Binary Tree"]
    parameters = ["p: Optional[TreeNode]", "q: Optional[TreeNode]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given the roots of two binary trees p and q, write a function to check if they are the same or not."

    def get_test_cases(self):
        return [
            TestCase({"p": [1,2,3], "q": [1,2,3]}, True, "Example 1"),
            TestCase({"p": [1,2], "q": [1,None,2]}, False, "Example 2"),
            TestCase({"p": [1,2,1], "q": [1,1,2]}, False, "Example 3"),
            TestCase({"p": [], "q": []}, True, "Both empty", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_SAME_TREE_TPL, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def eq(a,b):
            if a is None and b is None: return True
            if a is None or b is None: return False
            return a==b
        # Compare level-order lists directly
        def norm(lst):
            while lst and lst[-1] is None: lst.pop()
            return lst
        return norm(list(inputs["p"])) == norm(list(inputs["q"]))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            n = rng.randint(0, 8)
            base = [rng.randint(1,20) if rng.random()>0.2 else None for _ in range(n)]
            if base and base[0] is None: base[0]=1
            if i%2==0:
                tests.append({"p": base, "q": list(base)})
            else:
                other = [rng.randint(1,20) if rng.random()>0.2 else None for _ in range(n)]
                if other and other[0] is None: other[0]=1
                tests.append({"p": base, "q": other})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 572 — Subtree of Another Tree
# ═══════════════════════════════════════════════════════════════════════════
_SUBTREE_TPL = (
    "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
    "def main():\n"
    "    root = build_binary_tree({root})\n"
    "    subRoot = build_binary_tree({subRoot})\n"
    "    sol = Solution()\n"
    "    result = sol.isSubtree(root, subRoot)\n"
    "    print('__RESULT__:')\n"
    "    print(repr(result))\n\n"
    "main()\n"
)

class SubtreeOfAnotherTreePlugin(ProblemPlugin):
    problem_id = "subtree-of-another-tree"
    leetcode_number = 572
    title = "Subtree of Another Tree"
    slug = "subtree-of-another-tree"
    method_name = "isSubtree"
    difficulty = "Easy"
    pattern = "Trees"
    topics = ["Tree", "DFS", "Binary Tree", "String Matching"]
    parameters = ["root: Optional[TreeNode]", "subRoot: Optional[TreeNode]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values as subRoot."

    def get_test_cases(self):
        return [
            TestCase({"root": [3,4,5,1,2], "subRoot": [4,1,2]}, True, "Example 1"),
            TestCase({"root": [3,4,5,1,2,None,None,None,None,0], "subRoot": [4,1,2]}, False, "Example 2"),
            TestCase({"root": [1], "subRoot": [1]}, True, "Both same single", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_SUBTREE_TPL, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]
            q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        def same(a,b):
            if a is None and b is None: return True
            if a is None or b is None: return False
            return a.val==b.val and same(a.left,b.left) and same(a.right,b.right)
        def check(node, sub):
            if node is None: return False
            if same(node,sub): return True
            return check(node.left,sub) or check(node.right,sub)
        return check(build(inputs["root"]), build(inputs["subRoot"]))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            n = rng.randint(3, 10)
            root = [rng.randint(1,20) for _ in range(n)]
            m = rng.randint(1, 4)
            sub = [rng.randint(1,20) for _ in range(m)]
            tests.append({"root": root, "subRoot": sub})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 105 — Construct Binary Tree from Preorder and Inorder Traversal
# ═══════════════════════════════════════════════════════════════════════════
_CONSTRUCT_TPL = (
    "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
    "def main():\n"
    "    preorder = {preorder}\n"
    "    inorder  = {inorder}\n"
    "    sol = Solution()\n"
    "    result = sol.buildTree(preorder, inorder)\n"
    "    print('__RESULT__:')\n"
    "    print(repr(serialize_binary_tree(result)))\n\n"
    "main()\n"
)

class ConstructTreePreInPlugin(ProblemPlugin):
    problem_id = "construct-binary-tree-from-preorder-and-inorder-traversal"
    leetcode_number = 105
    title = "Construct Binary Tree from Preorder and Inorder Traversal"
    slug = "construct-binary-tree-from-preorder-and-inorder-traversal"
    method_name = "buildTree"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Array", "Hash Table", "Divide and Conquer", "Tree", "Binary Tree"]
    parameters = ["preorder: List[int]", "inorder: List[int]"]
    return_type = "Optional[TreeNode]"
    hidden_test_count = 4
    description = "Given two integer arrays preorder and inorder, construct and return the binary tree."

    def get_test_cases(self):
        return [
            TestCase({"preorder":[3,9,20,15,7],"inorder":[9,3,15,20,7]},
                     [3,9,20,None,None,15,7], "Example 1"),
            TestCase({"preorder":[-1],"inorder":[-1]}, [-1], "Single node"),
            TestCase({"preorder":[1,2,3],"inorder":[2,1,3]}, [1,2,3], "Balanced", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_CONSTRUCT_TPL, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        pre, ino = list(inputs["preorder"]), list(inputs["inorder"])
        if not pre: return []
        def build(pre, ino):
            if not pre: return None
            root_val = pre[0]
            idx = ino.index(root_val)
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            node = N(root_val)
            node.left = build(pre[1:idx+1], ino[:idx])
            node.right = build(pre[idx+1:], ino[idx+1:])
            return node
        def serialize(root):
            if not root: return []
            from collections import deque
            result=[]; q=deque([root])
            while q:
                n=q.popleft()
                if n is None: result.append(None); continue
                result.append(n.val); q.append(n.left); q.append(n.right)
            while result and result[-1] is None: result.pop()
            return result
        return serialize(build(pre, ino))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 8)
            vals = rng.sample(range(1,50), n)
            # Build random BST-ish to get valid pre/inorder
            import random
            inorder = sorted(vals)
            def build_pre(inorder):
                if not inorder: return []
                mid = rng.randint(0, len(inorder)-1)
                return [inorder[mid]] + build_pre(inorder[:mid]) + build_pre(inorder[mid+1:])
            preorder = build_pre(inorder)
            tests.append({"preorder": preorder, "inorder": inorder})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 235 — Lowest Common Ancestor of BST
# ═══════════════════════════════════════════════════════════════════════════
_LCA_BST_TPL = (
    "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
    "def main():\n"
    "    root = build_binary_tree({root})\n"
    "    # find p and q nodes by value\n"
    "    def find(node, v):\n"
    "        if not node: return None\n"
    "        if node.val==v: return node\n"
    "        return find(node.left,v) or find(node.right,v)\n"
    "    p = find(root, {p})\n"
    "    q = find(root, {q})\n"
    "    sol = Solution()\n"
    "    result = sol.lowestCommonAncestor(root, p, q)\n"
    "    print('__RESULT__:')\n"
    "    print(repr(result.val if result else None))\n\n"
    "main()\n"
)

class LCABSTPlugin(ProblemPlugin):
    problem_id = "lowest-common-ancestor-of-a-binary-search-tree"
    leetcode_number = 235
    title = "Lowest Common Ancestor of a Binary Search Tree"
    slug = "lowest-common-ancestor-of-a-binary-search-tree"
    method_name = "lowestCommonAncestor"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BST", "Binary Search Tree", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]", "p: Optional[TreeNode]", "q: Optional[TreeNode]"]
    return_type = "Optional[TreeNode]"
    hidden_test_count = 4
    description = "Given a BST, find the lowest common ancestor (LCA) of two given nodes p and q."

    def get_test_cases(self):
        return [
            TestCase({"root":[6,2,8,0,4,7,9,None,None,3,5],"p":2,"q":8}, 6, "Example 1"),
            TestCase({"root":[6,2,8,0,4,7,9,None,None,3,5],"p":2,"q":4}, 2, "Example 2"),
            TestCase({"root":[2,1],"p":2,"q":1}, 2, "Example 3"),
            TestCase({"root":[4,2,6,1,3,5,7],"p":1,"q":3}, 2, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_LCA_BST_TPL, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        root_vals = inputs["root"]
        pv, qv = inputs["p"], inputs["q"]
        # For BST: traverse by value
        def lca(vals, p, q):
            from collections import deque
            if not vals: return None
            # BST lca by value navigation
            cur = vals[0]
            if p <= cur <= q or q <= cur <= p:
                return cur
            if p < cur and q < cur:
                # go left — find left subtree
                left = []
                idx = 1
                level_size = 1
                i = 1
                # BFS level-order: left child is at 2*i+1 for 0-indexed
                def left_subtree(items):
                    if len(items) < 2: return []
                    result = [items[1]] if items[1] is not None else []
                    # collect all descendants of index 1
                    queue = deque([1])
                    out = []
                    while queue:
                        x = queue.popleft()
                        if x >= len(items): continue
                        if items[x] is not None: out.append(items[x])
                        queue.append(2*x+1); queue.append(2*x+2)
                    return out
                return lca(left_subtree(vals), p, q)
            else:
                def right_subtree(items):
                    if len(items) < 3: return []
                    queue = deque([2])
                    out = []
                    while queue:
                        x = queue.popleft()
                        if x >= len(items): continue
                        if items[x] is not None: out.append(items[x])
                        queue.append(2*x+1); queue.append(2*x+2)
                    return out
                return lca(right_subtree(vals), p, q)
        # Simpler: use BST property directly on values
        cur = root_vals[0]
        # Walk sorted bst by value
        # Since root_vals is level-order, just use value comparison for BST
        node_val = root_vals[0]
        pv2, qv2 = min(pv, qv), max(pv, qv)
        # walk by BST value logic using the root array
        vals = root_vals
        idx = 0
        while idx < len(vals) and vals[idx] is not None:
            cur = vals[idx]
            if pv2 <= cur <= qv2:
                return cur
            elif cur > qv2:
                idx = 2*idx+1
            else:
                idx = 2*idx+2
        return None

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            # Build valid BST as level-order list
            n = rng.randint(3, 10)
            vals = sorted(rng.sample(range(1, 50), n))
            # Level-order BST
            def bst_level_order(sorted_vals):
                if not sorted_vals: return []
                result = []
                from collections import deque
                q = deque([(sorted_vals, 0)])
                level_map = {}
                def build(sv):
                    if not sv: return
                    mid = len(sv)//2
                    result.append(sv[mid])
                    build(sv[:mid]); build(sv[mid+1:])
                build(vals)
                return result
            tree = bst_level_order(vals)
            p, q = rng.sample(vals, 2)
            tests.append({"root": tree, "p": p, "q": q})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 102 — Binary Tree Level Order Traversal
# ═══════════════════════════════════════════════════════════════════════════
class LevelOrderTraversalPlugin(ProblemPlugin):
    problem_id = "binary-tree-level-order-traversal"
    leetcode_number = 102
    title = "Binary Tree Level Order Traversal"
    slug = "binary-tree-level-order-traversal"
    method_name = "levelOrder"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Tree", "BFS", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "List[List[int]]"
    hidden_test_count = 4
    description = "Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level)."

    def get_test_cases(self):
        return [
            TestCase({"root": [3,9,20,None,None,15,7]}, [[3],[9,20],[15,7]], "Example 1"),
            TestCase({"root": [1]}, [[1]], "Single node"),
            TestCase({"root": []}, [], "Empty tree"),
            TestCase({"root": [1,2,3,4,5]}, [[1],[2,3],[4,5]], "Complete tree", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("levelOrder", [("root","tree")], out_type="list")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        items = inputs["root"]
        if not items: return []
        from collections import deque
        class N:
            def __init__(self,v): self.val=v; self.left=self.right=None
        nodes=[None if v is None else N(v) for v in items]
        q=deque([0]); i=1
        while q and i<len(nodes):
            idx=q.popleft()
            if nodes[idx] is None: continue
            if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
            if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
        result=[]; bfsq=deque([nodes[0]])
        while bfsq:
            level=[]; sz=len(bfsq)
            for _ in range(sz):
                n=bfsq.popleft()
                if n: level.append(n.val);bfsq.append(n.left);bfsq.append(n.right)
            if level: result.append(level)
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(0, 12)
            vals = [rng.randint(1,50) if rng.random()>0.15 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=1
            tests.append({"root": vals})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 98 — Validate Binary Search Tree
# ═══════════════════════════════════════════════════════════════════════════
class ValidateBSTPlugin(ProblemPlugin):
    problem_id = "validate-binary-search-tree"
    leetcode_number = 98
    title = "Validate Binary Search Tree"
    slug = "validate-binary-search-tree"
    method_name = "isValidBST"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BST", "Binary Search Tree", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Given the root of a binary tree, determine if it is a valid binary search tree (BST)."

    def get_test_cases(self):
        return [
            TestCase({"root": [2,1,3]}, True, "Example 1"),
            TestCase({"root": [5,1,4,None,None,3,6]}, False, "Example 2"),
            TestCase({"root": [2,2,2]}, False, "Duplicates invalid"),
            TestCase({"root": [1]}, True, "Single node", is_hidden=True),
            TestCase({"root": [5,4,6,None,None,3,7]}, False, "Tricky invalid", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("isValidBST", [("root","tree")], out_type="bool")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]
            q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        def valid(node, lo=float('-inf'), hi=float('inf')):
            if not node: return True
            if node.val<=lo or node.val>=hi: return False
            return valid(node.left,lo,node.val) and valid(node.right,node.val,hi)
        return valid(build(inputs["root"]))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for i in range(count):
            n = rng.randint(1, 10)
            if i%2==0:  # valid BST
                vals = sorted(rng.sample(range(1,50), min(n,49)))
                def bst_lo(sv):
                    if not sv: return []
                    mid=len(sv)//2
                    return [sv[mid]]+bst_lo(sv[:mid])+bst_lo(sv[mid+1:])
                tree = bst_lo(vals)
            else:        # invalid BST
                tree = [rng.randint(1,20) for _ in range(n)]
            tests.append({"root": tree})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 230 — Kth Smallest Element in a BST
# ═══════════════════════════════════════════════════════════════════════════
class KthSmallestBSTPlugin(ProblemPlugin):
    problem_id = "kth-smallest-element-in-a-bst"
    leetcode_number = 230
    title = "Kth Smallest Element in a BST"
    slug = "kth-smallest-element-in-a-bst"
    method_name = "kthSmallest"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BST", "Binary Search Tree", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]", "k: int"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given the root of a binary search tree and an integer k, return the kth smallest value (1-indexed) of all values of nodes in the tree."

    def get_test_cases(self):
        return [
            TestCase({"root":[3,1,4,None,2],"k":1}, 1, "Example 1"),
            TestCase({"root":[5,3,6,2,4,None,None,1],"k":3}, 3, "Example 2"),
            TestCase({"root":[1],"k":1}, 1, "Single node", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = (
            "{imports}\n\n{helpers}\n\n{solution_code}\n\n"
            "def main():\n"
            "    root = build_binary_tree({root})\n"
            "    sol = Solution()\n"
            "    result = sol.kthSmallest(root, {k})\n"
            "    print('__RESULT__:')\n"
            "    print(repr(result))\n\n"
            "main()\n"
        )
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]
            q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        vals=[]
        def inorder(n):
            if not n: return
            inorder(n.left); vals.append(n.val); inorder(n.right)
        inorder(build(inputs["root"]))
        return vals[inputs["k"]-1]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 10)
            vals = sorted(rng.sample(range(1,50), min(n,49)))
            def bst_lo(sv):
                if not sv: return []
                mid=len(sv)//2
                return [sv[mid]]+bst_lo(sv[:mid])+bst_lo(sv[mid+1:])
            tree = bst_lo(vals)
            k = rng.randint(1, len(vals))
            tests.append({"root": tree, "k": k})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 199 — Binary Tree Right Side View
# ═══════════════════════════════════════════════════════════════════════════
class RightSideViewPlugin(ProblemPlugin):
    problem_id = "binary-tree-right-side-view"
    leetcode_number = 199
    title = "Binary Tree Right Side View"
    slug = "binary-tree-right-side-view"
    method_name = "rightSideView"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BFS", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = "Given the root of a binary tree, imagine yourself standing on the right side of it. Return the values of the nodes you can see ordered from top to bottom."

    def get_test_cases(self):
        return [
            TestCase({"root": [1,2,3,None,5,None,4]}, [1,3,4], "Example 1"),
            TestCase({"root": [1,None,3]}, [1,3], "Example 2"),
            TestCase({"root": []}, [], "Empty tree"),
            TestCase({"root": [1,2,3,4,5,6,7]}, [1,3,7], "Full tree", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("rightSideView", [("root","tree")], out_type="list")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        items = inputs["root"]
        if not items: return []
        from collections import deque
        class N:
            def __init__(self,v): self.val=v; self.left=self.right=None
        nodes=[None if v is None else N(v) for v in items]
        q=deque([0]); i=1
        while q and i<len(nodes):
            idx=q.popleft()
            if nodes[idx] is None: continue
            if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
            if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
        result=[]; bfsq=deque([nodes[0]])
        while bfsq:
            sz=len(bfsq); last=None
            for _ in range(sz):
                n=bfsq.popleft()
                if n: last=n.val;bfsq.append(n.left);bfsq.append(n.right)
            if last is not None: result.append(last)
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(0, 12)
            vals = [rng.randint(1,50) if rng.random()>0.15 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=1
            tests.append({"root": vals})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 1448 — Count Good Nodes in Binary Tree
# ═══════════════════════════════════════════════════════════════════════════
class CountGoodNodesPlugin(ProblemPlugin):
    problem_id = "count-good-nodes-in-binary-tree"
    leetcode_number = 1448
    title = "Count Good Nodes in Binary Tree"
    slug = "count-good-nodes-in-binary-tree"
    method_name = "goodNodes"
    difficulty = "Medium"
    pattern = "Trees"
    topics = ["Tree", "DFS", "BFS", "Binary Tree"]
    parameters = ["root: TreeNode"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X. Return the number of good nodes in the binary tree."

    def get_test_cases(self):
        return [
            TestCase({"root": [3,1,4,3,None,1,5]}, 4, "Example 1"),
            TestCase({"root": [3,3,None,4,2]}, 3, "Example 2"),
            TestCase({"root": [1]}, 1, "Single node"),
            TestCase({"root": [2,None,4,10,8,None,None,4]}, 4, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("goodNodes", [("root","tree")], out_type="int")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]
            q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        count=[0]
        def dfs(node, max_so_far):
            if not node: return
            if node.val >= max_so_far: count[0]+=1
            dfs(node.left, max(max_so_far, node.val))
            dfs(node.right, max(max_so_far, node.val))
        dfs(build(inputs["root"]), float('-inf'))
        return count[0]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 12)
            vals = [rng.randint(1,20) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,20)
            tests.append({"root": vals})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 124 — Binary Tree Maximum Path Sum
# ═══════════════════════════════════════════════════════════════════════════
class MaxPathSumPlugin(ProblemPlugin):
    problem_id = "binary-tree-maximum-path-sum"
    leetcode_number = 124
    title = "Binary Tree Maximum Path Sum"
    slug = "binary-tree-maximum-path-sum"
    method_name = "maxPathSum"
    difficulty = "Hard"
    pattern = "Trees"
    topics = ["Dynamic Programming", "Tree", "DFS", "Binary Tree"]
    parameters = ["root: Optional[TreeNode]"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given the root of a binary tree, return the maximum path sum of any non-empty path."

    def get_test_cases(self):
        return [
            TestCase({"root": [1,2,3]}, 6, "Example 1"),
            TestCase({"root": [-3]}, -3, "Single negative"),
            TestCase({"root": [-10,9,20,None,None,15,7]}, 42, "Example 2"),
            TestCase({"root": [1,-2,3]}, 4, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        tpl = _tree_tpl("maxPathSum", [("root","tree")], out_type="int")
        return WrapperTemplate(template_str=tpl, helpers_str=TREE_NODE_HELPERS)

    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]
            q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        best=[float('-inf')]
        def dfs(node):
            if not node: return 0
            l=max(dfs(node.left),0); r=max(dfs(node.right),0)
            best[0]=max(best[0], node.val+l+r)
            return node.val+max(l,r)
        dfs(build(inputs["root"]))
        return best[0]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 12)
            vals = [rng.randint(-20,20) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(-20,20)
            tests.append({"root": vals})
        return tests
