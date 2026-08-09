"""Batch 5 — NeetCode 250: more arrays, strings, linked lists, and trees."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, Validator, ValidationResult
)
from backend.execution_engine.object_builder import LIST_NODE_HELPERS, TREE_NODE_HELPERS

# LC 160 — Intersection of Two Linked Lists
_LL_INTERSECT_TPL = """{imports}
{helpers}
{solution_code}

def main():
    la = build_linked_list({listA})
    lb = build_linked_list({listB})
    # set up intersection if skipA/skipB indicate one
    skipA = {skipA}; skipB = {skipB}
    nodeA = la; nodeB = lb
    for _ in range(skipA):
        if nodeA: nodeA = nodeA.next
    for _ in range(skipB):
        if nodeB: nodeB = nodeB.next
    if nodeA and nodeB:
        # find end of la and point to nodeB
        cur = la
        while cur and cur.next: cur = cur.next
        if cur: cur.next = nodeB
    sol = Solution()
    result = sol.getIntersectionNode(la, lb)
    print("__RESULT__:")
    print(repr(result.val if result else None))

main()
"""

class IntersectionOfTwoLinkedListsPlugin(ProblemPlugin):
    problem_id="intersection-of-two-linked-lists"; leetcode_number=160
    title="Intersection of Two Linked Lists"; slug="intersection-of-two-linked-lists"
    method_name="getIntersectionNode"; difficulty="Easy"; pattern="Linked List"
    topics=["Hash Table","Linked List","Two Pointers"]
    parameters=["headA: ListNode","headB: ListNode"]; return_type="Optional[ListNode]"; hidden_test_count=3
    description="Return the node at which two linked lists intersect, or null."
    def get_test_cases(self):
        return [
            TestCase({"listA":[4,1,8,4,5],"listB":[5,6,1,8,4,5],"skipA":2,"skipB":3},8,"Example 1"),
            TestCase({"listA":[1,9,1,2,4],"listB":[3,2,4],"skipA":3,"skipB":1},2,"Example 2"),
            TestCase({"listA":[2,6,4],"listB":[1,5],"skipA":3,"skipB":2},None,"Example 3: no intersect"),
        ]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_LL_INTERSECT_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        la,lb=inputs["listA"],inputs["listB"]
        skipA,skipB=inputs["skipA"],inputs["skipB"]
        if skipA>=len(la) or skipB>=len(lb): return None
        if la[skipA:] == lb[skipB:]: return la[skipA]
        return None
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            if i%2==0:
                common=[rng.randint(1,9) for _ in range(rng.randint(1,3))]
                pre_a=[rng.randint(1,9) for _ in range(rng.randint(1,3))]
                pre_b=[rng.randint(1,9) for _ in range(rng.randint(1,3))]
                tests.append({"listA":pre_a+common,"listB":pre_b+common,"skipA":len(pre_a),"skipB":len(pre_b)})
            else:
                tests.append({"listA":[1,2,3],"listB":[4,5],"skipA":3,"skipB":2})
        return tests


# LC 234 — Palindrome Linked List
_PALIN_LL_TPL = """{imports}
{helpers}
{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.isPalindrome(head)
    print("__RESULT__:")
    print(repr(result))

main()
"""
class PalindromeLinkedListPlugin(ProblemPlugin):
    problem_id="palindrome-linked-list"; leetcode_number=234
    title="Palindrome Linked List"; slug="palindrome-linked-list"
    method_name="isPalindrome"; difficulty="Easy"; pattern="Linked List"
    topics=["Linked List","Two Pointers","Stack","Recursion"]
    parameters=["head: Optional[ListNode]"]; return_type="bool"; hidden_test_count=4
    description="Return true if the linked list is a palindrome."
    def get_test_cases(self):
        return [TestCase({"head":[1,2,2,1]},True,"Example 1"),TestCase({"head":[1,2]},False,"Example 2"),
                TestCase({"head":[1]},True,"Single",is_hidden=True),TestCase({"head":[1,2,1]},True,"Odd palindrome",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_PALIN_LL_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs): vals=inputs["head"]; return vals==vals[::-1]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            if i%2==0:
                half=[rng.randint(1,9) for _ in range(rng.randint(1,5))]
                vals=half+half[::-1]
            else:
                vals=[rng.randint(1,9) for _ in range(rng.randint(2,8))]
            tests.append({"head":vals})
        return tests


# LC 148 — Sort List
_SORT_LIST_TPL = """{imports}
{helpers}
{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.sortList(head)
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""
class SortListPlugin(ProblemPlugin):
    problem_id="sort-list"; leetcode_number=148
    title="Sort List"; slug="sort-list"
    method_name="sortList"; difficulty="Medium"; pattern="Linked List"
    topics=["Linked List","Two Pointers","Divide and Conquer","Sorting","Merge Sort"]
    parameters=["head: Optional[ListNode]"]; return_type="Optional[ListNode]"; hidden_test_count=4
    description="Sort the linked list in O(n log n) time and O(1) memory."
    def get_test_cases(self):
        return [TestCase({"head":[4,2,1,3]},[1,2,3,4],"Example 1"),TestCase({"head":[-1,5,3,4,0]},[-1,0,3,4,5],"Example 2"),
                TestCase({"head":[]},[],None,is_hidden=True),TestCase({"head":[1]},[1],"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_SORT_LIST_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs): return sorted(inputs["head"])
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"head":[rng.randint(-20,20) for _ in range(rng.randint(0,12))]} for _ in range(count)]


# LC 83 — Remove Duplicates from Sorted List
_REM_DUPS_LL_TPL = """{imports}
{helpers}
{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.deleteDuplicates(head)
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""
class RemoveDuplicatesSortedListPlugin(ProblemPlugin):
    problem_id="remove-duplicates-from-sorted-list"; leetcode_number=83
    title="Remove Duplicates from Sorted List"; slug="remove-duplicates-from-sorted-list"
    method_name="deleteDuplicates"; difficulty="Easy"; pattern="Linked List"
    topics=["Linked List"]; parameters=["head: Optional[ListNode]"]; return_type="Optional[ListNode]"; hidden_test_count=4
    description="Delete all duplicates such that each element appears only once."
    def get_test_cases(self):
        return [TestCase({"head":[1,1,2]},[1,2],"Example 1"),TestCase({"head":[1,1,2,3,3]},[1,2,3],"Example 2"),
                TestCase({"head":[]},[],None,is_hidden=True),TestCase({"head":[1,1,1]},[1],"All same",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_REM_DUPS_LL_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        from collections import OrderedDict
        seen=OrderedDict(); [seen.setdefault(v,True) for v in inputs["head"]]
        return list(seen.keys())
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"head":sorted([rng.randint(1,5) for _ in range(rng.randint(0,10))])} for _ in range(count)]


# LC 61 — Rotate List
_ROTATE_LIST_TPL = """{imports}
{helpers}
{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.rotateRight(head, {k})
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""
class RotateListPlugin(ProblemPlugin):
    problem_id="rotate-list"; leetcode_number=61
    title="Rotate List"; slug="rotate-list"; method_name="rotateRight"; difficulty="Medium"; pattern="Linked List"
    topics=["Linked List","Two Pointers"]; parameters=["head: Optional[ListNode]","k: int"]
    return_type="Optional[ListNode]"; hidden_test_count=4; description="Rotate the list to the right by k places."
    def get_test_cases(self):
        return [TestCase({"head":[1,2,3,4,5],"k":2},[4,5,1,2,3],"Example 1"),
                TestCase({"head":[0,1,2],"k":4},[2,0,1],"Example 2"),
                TestCase({"head":[],"k":0},[],"Empty list",is_hidden=True),TestCase({"head":[1,2],"k":1},[2,1],"Two elements",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_ROTATE_LIST_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        vals=inputs["head"]; k=inputs["k"]
        if not vals: return []
        n=len(vals); k%=n; return vals[-k:]+vals[:-k] if k else vals
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"head":[rng.randint(0,9) for _ in range(rng.randint(0,8))],"k":rng.randint(0,10)} for _ in range(count)]


# LC 112 — Path Sum
_PATH_SUM_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    result = sol.hasPathSum(root, {targetSum})
    print("__RESULT__:")
    print(repr(result))

main()
"""
class PathSumPlugin(ProblemPlugin):
    problem_id="path-sum"; leetcode_number=112
    title="Path Sum"; slug="path-sum"; method_name="hasPathSum"; difficulty="Easy"; pattern="Trees"
    topics=["Tree","DFS","BFS","Binary Tree"]; parameters=["root: Optional[TreeNode]","targetSum: int"]
    return_type="bool"; hidden_test_count=4; description="Return true if there is a root-to-leaf path summing to targetSum."
    def get_test_cases(self):
        return [TestCase({"root":[5,4,8,11,None,13,4,7,2,None,None,None,1],"targetSum":22},True,"Example 1"),
                TestCase({"root":[1,2,3],"targetSum":5},False,"Example 2"),
                TestCase({"root":[],"targetSum":0},False,"Empty"),TestCase({"root":[1],"targetSum":1},True,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_PATH_SUM_TPL, helpers_str=TREE_NODE_HELPERS)
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
        def dfs(node, rem):
            if not node: return False
            rem-=node.val
            if not node.left and not node.right: return rem==0
            return dfs(node.left,rem) or dfs(node.right,rem)
        return dfs(build(inputs["root"]), inputs["targetSum"])
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,10)
            vals=[rng.randint(1,20) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,20)
            target=rng.randint(1,50)
            tests.append({"root":vals,"targetSum":target})
        return tests


# LC 113 — Path Sum II
_PATH_SUM_II_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    result = sol.pathSum(root, {targetSum})
    print("__RESULT__:")
    print(repr(result))

main()
"""
class PathSumIIPlugin(ProblemPlugin):
    problem_id="path-sum-ii"; leetcode_number=113
    title="Path Sum II"; slug="path-sum-ii"; method_name="pathSum"; difficulty="Medium"; pattern="Trees"
    topics=["Backtracking","Tree","DFS","Binary Tree"]; parameters=["root: Optional[TreeNode]","targetSum: int"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Return all root-to-leaf paths where sum equals targetSum."
    def get_test_cases(self):
        return [TestCase({"root":[5,4,8,11,None,13,4,7,2,None,None,5,1],"targetSum":22},[[5,4,11,2],[5,8,4,5]],"Example 1"),
                TestCase({"root":[1,2,3],"targetSum":5},[],"Example 2"),TestCase({"root":[],"targetSum":0},[],"Empty")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import AnyOrderListValidator; return AnyOrderListValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_PATH_SUM_II_TPL, helpers_str=TREE_NODE_HELPERS)
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
        result=[]
        def dfs(node,path,rem):
            if not node: return
            path.append(node.val); rem-=node.val
            if not node.left and not node.right and rem==0: result.append(path[:])
            dfs(node.left,path,rem); dfs(node.right,path,rem); path.pop()
        dfs(build(inputs["root"]),[],inputs["targetSum"]); return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,10); vals=[rng.randint(1,10) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,10)
            tests.append({"root":vals,"targetSum":rng.randint(5,30)})
        return tests


# LC 116 — Populating Next Right Pointers in Each Node
_NEXT_RIGHT_TPL = """{imports}
{helpers}

class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val; self.left = left; self.right = right; self.next = next

{solution_code}

def main():
    items = {root}
    if not items:
        root = None
    else:
        nodes = [Node(v) if v is not None else None for v in items]
        for i in range(len(nodes)):
            if nodes[i] is None: continue
            l, r = 2*i+1, 2*i+2
            if l < len(nodes): nodes[i].left = nodes[l]
            if r < len(nodes): nodes[i].right = nodes[r]
        root = nodes[0]
    sol = Solution()
    result = sol.connect(root)
    # Serialize: collect next pointers level by level
    out = []
    from collections import deque
    q = deque([root]) if root else deque()
    while q:
        level_size = len(q)
        for i in range(level_size):
            n = q.popleft()
            if n:
                out.append(n.val)
                if i == level_size-1: out.append('#')
                if n.left: q.append(n.left)
                if n.right: q.append(n.right)
    print("__RESULT__:")
    print(repr(out))

main()
"""
class PopulatingNextRightPointersPlugin(ProblemPlugin):
    problem_id="populating-next-right-pointers-in-each-node"; leetcode_number=116
    title="Populating Next Right Pointers in Each Node"; slug="populating-next-right-pointers-in-each-node"
    method_name="connect"; difficulty="Medium"; pattern="Trees"
    topics=["Linked List","Tree","DFS","BFS","Binary Tree"]; parameters=["root: Optional[Node]"]
    return_type="Optional[Node]"; hidden_test_count=3; description="Connect each node's next pointer to its right neighbor."
    def get_test_cases(self):
        return [TestCase({"root":[1,2,3,4,5,6,7]},[1,'#',2,3,'#',4,5,6,7,'#'],"Example 1"),
                TestCase({"root":[]},[],"Empty"),TestCase({"root":[1]},[1,'#'],"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_NEXT_RIGHT_TPL)
    @staticmethod
    def oracle(inputs):
        items=inputs["root"]
        if not items: return []
        result=[]
        from collections import deque
        levels=[]; n=len(items); i=0; level_size=1
        while i<n:
            level=[v for v in items[i:i+level_size] if v is not None or i+level_size<=n]
            actual=[v for v in items[i:i+level_size]]
            result.extend(v for v in actual if v is not None)
            result.append('#')
            i+=level_size; level_size*=2
            if all(v is None for v in items[i:] if i<n): break
        while result and result[-1]=='#' and len(result)>1 and result[-2]=='#': result.pop()
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            levels=rng.randint(2,4); vals=[1]
            for _ in range(levels-1): vals.extend([rng.randint(1,20)]*( 2**len(vals).bit_length() if len(vals)>0 else 1))
            # just build a simple perfect binary tree
            total=2**levels-1; tests.append({"root":list(range(1,total+1))})
        return tests


# LC 222 — Count Complete Tree Nodes
_COUNT_NODES_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    result = sol.countNodes(root)
    print("__RESULT__:")
    print(repr(result))

main()
"""
class CountCompleteTreeNodesPlugin(ProblemPlugin):
    problem_id="count-complete-tree-nodes"; leetcode_number=222
    title="Count Complete Tree Nodes"; slug="count-complete-tree-nodes"
    method_name="countNodes"; difficulty="Easy"; pattern="Trees"
    topics=["Binary Search","Tree","DFS","BFS","Binary Tree"]
    parameters=["root: Optional[TreeNode]"]; return_type="int"; hidden_test_count=4
    description="Given the root of a complete binary tree, return the number of nodes."
    def get_test_cases(self):
        return [TestCase({"root":[1,2,3,4,5,6]},6,"Example 1"),TestCase({"root":[]},0,"Empty"),
                TestCase({"root":[1]},1,"Single",is_hidden=True),TestCase({"root":[1,2,3,4,5,6,7]},7,"Full",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_COUNT_NODES_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs): return sum(1 for v in inputs["root"] if v is not None)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(0,15); tests.append({"root":list(range(1,n+1))})
        return tests


# LC 257 — Binary Tree Paths
_BT_PATHS_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    result = sol.binaryTreePaths(root)
    print("__RESULT__:")
    print(repr(sorted(result)))

main()
"""
class BinaryTreePathsPlugin(ProblemPlugin):
    problem_id="binary-tree-paths"; leetcode_number=257
    title="Binary Tree Paths"; slug="binary-tree-paths"
    method_name="binaryTreePaths"; difficulty="Easy"; pattern="Trees"
    topics=["String","Backtracking","Tree","DFS","Binary Tree"]
    parameters=["root: Optional[TreeNode]"]; return_type="List[str]"; hidden_test_count=4
    description="Return all paths from root to leaves."
    def get_test_cases(self):
        return [TestCase({"root":[1,2,3,None,5]},["1->2->5","1->3"],"Example 1"),
                TestCase({"root":[1]},["1"],"Single")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import SetValidator; return SetValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_BT_PATHS_TPL, helpers_str=TREE_NODE_HELPERS)
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
        paths=[]
        def dfs(node,path):
            if not node: return
            path.append(str(node.val))
            if not node.left and not node.right: paths.append("->".join(path))
            dfs(node.left,path); dfs(node.right,path); path.pop()
        dfs(build(inputs["root"]),[]); return paths
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,8); vals=[rng.randint(1,20) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,20)
            tests.append({"root":vals})
        return tests
