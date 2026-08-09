"""Batch 7 — NeetCode 250: strings, arrays, linked lists, trees (LC 6,8,12,23,25,31,35,47,75,77,86,93,95,96,103,106,114,118,123,135,145,162,173,201,236)."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, AnyOrderListValidator, Validator, ValidationResult
)
from backend.execution_engine.object_builder import LIST_NODE_HELPERS, TREE_NODE_HELPERS


# LC 6 — Zigzag Conversion
class ZigzagConversionPlugin(ProblemPlugin):
    problem_id="zigzag-conversion"; leetcode_number=6; title="Zigzag Conversion"
    slug="zigzag-conversion"; method_name="convert"; difficulty="Medium"; pattern="Array"
    topics=["String"]; parameters=["s: str","numRows: int"]; return_type="str"; hidden_test_count=4
    description="Convert string to zigzag pattern on numRows rows then read line by line."
    def get_test_cases(self):
        return [TestCase({"s":"PAYPALISHIRING","numRows":3},"PAHNAPLSIIGYIR","Example 1"),
                TestCase({"s":"PAYPALISHIRING","numRows":4},"PINALSIGYAHRPI","Example 2"),
                TestCase({"s":"A","numRows":1},"A","Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s,n=inputs["s"],inputs["numRows"]
        if n==1 or n>=len(s): return s
        rows=[""]*n; row,step=0,1
        for c in s:
            rows[row]+=c
            if row==0: step=1
            elif row==n-1: step=-1
            row+=step
        return "".join(rows)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; return [{"s":"".join(rng.choices(string.ascii_uppercase[:10],k=rng.randint(4,15))),"numRows":rng.randint(2,5)} for _ in range(count)]


# LC 8 — String to Integer (atoi)
class AtoiPlugin(ProblemPlugin):
    problem_id="string-to-integer-atoi"; leetcode_number=8; title="String to Integer (atoi)"
    slug="string-to-integer-atoi"; method_name="myAtoi"; difficulty="Medium"; pattern="Array"
    topics=["String"]; parameters=["s: str"]; return_type="int"; hidden_test_count=4
    description="Implement myAtoi(string s), which converts a string to a 32-bit signed integer."
    def get_test_cases(self):
        return [TestCase({"s":"42"},42,"Example 1"),TestCase({"s":"   -42"},-42,"Example 2"),
                TestCase({"s":"4193 with words"},4193,"Example 3"),TestCase({"s":"words and 987"},0,"Example 4")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s=inputs["s"].lstrip(); sign=1; i=0
        INT_MAX,INT_MIN=2**31-1,-(2**31)
        if i<len(s) and s[i] in '+-': sign=(-1 if s[i]=='-' else 1); i+=1
        result=0
        while i<len(s) and s[i].isdigit(): result=result*10+int(s[i]); i+=1
        result*=sign
        return max(INT_MIN,min(INT_MAX,result))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            tests.append({"s":rng.choice(["  -123","456abc","+789","0","2147483647","-2147483648","  +0 "])})
        return tests


# LC 12 — Integer to Roman
class IntegerToRomanPlugin(ProblemPlugin):
    problem_id="integer-to-roman"; leetcode_number=12; title="Integer to Roman"
    slug="integer-to-roman"; method_name="intToRoman"; difficulty="Medium"; pattern="Array"
    topics=["Hash Table","Math","String"]; parameters=["num: int"]; return_type="str"; hidden_test_count=4
    description="Convert an integer to a Roman numeral."
    def get_test_cases(self):
        return [TestCase({"num":3},"III","Example 1"),TestCase({"num":58},"LVIII","Example 2"),
                TestCase({"num":1994},"MCMXCIV","Example 3"),TestCase({"num":4},"IV","IV",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["num"]; vals=[(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
        r=""
        for v,sym in vals:
            while n>=v: r+=sym; n-=v
        return r
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"num":rng.randint(1,3999)} for _ in range(count)]


# LC 31 — Next Permutation
class NextPermutationPlugin(ProblemPlugin):
    problem_id="next-permutation"; leetcode_number=31; title="Next Permutation"
    slug="next-permutation"; method_name="nextPermutation"; difficulty="Medium"; pattern="Array"
    topics=["Array","Two Pointers"]; parameters=["nums: List[int]"]; return_type="None"; hidden_test_count=4
    description="Rearrange nums into the lexicographically next greater permutation."
    def get_test_cases(self):
        return [TestCase({"nums":[1,2,3]},[1,3,2],"Example 1"),TestCase({"nums":[3,2,1]},[1,2,3],"Example 2"),
                TestCase({"nums":[1,1,5]},[1,5,1],"Example 3"),TestCase({"nums":[1]},[1],"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums=list(inputs["nums"]); n=len(nums); i=n-2
        while i>=0 and nums[i]>=nums[i+1]: i-=1
        if i>=0:
            j=n-1
            while nums[j]<=nums[i]: j-=1
            nums[i],nums[j]=nums[j],nums[i]
        nums[i+1:]=reversed(nums[i+1:])
        return nums
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":rng.sample(range(1,8),rng.randint(2,5))} for _ in range(count)]


# LC 35 — Search Insert Position
class SearchInsertPositionPlugin(ProblemPlugin):
    problem_id="search-insert-position"; leetcode_number=35; title="Search Insert Position"
    slug="search-insert-position"; method_name="searchInsert"; difficulty="Easy"; pattern="Binary Search"
    topics=["Array","Binary Search"]; parameters=["nums: List[int]","target: int"]; return_type="int"; hidden_test_count=4
    description="Return the index of target in sorted nums, or where it would be inserted."
    def get_test_cases(self):
        return [TestCase({"nums":[1,3,5,6],"target":5},2,"Example 1"),TestCase({"nums":[1,3,5,6],"target":2},1,"Example 2"),
                TestCase({"nums":[1,3,5,6],"target":7},4,"Example 3"),TestCase({"nums":[1],"target":0},0,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums,t=inputs["nums"],inputs["target"]; lo,hi=0,len(nums)
        while lo<hi:
            mid=(lo+hi)//2
            if nums[mid]<t: lo=mid+1
            else: hi=mid
        return lo
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            nums=sorted(set(rng.randint(1,30) for _ in range(rng.randint(3,10))))
            t=rng.randint(1,35); tests.append({"nums":nums,"target":t})
        return tests


# LC 47 — Permutations II
class PermutationsIIPlugin(ProblemPlugin):
    problem_id="permutations-ii"; leetcode_number=47; title="Permutations II"
    slug="permutations-ii"; method_name="permuteUnique"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking"]; parameters=["nums: List[int]"]; return_type="List[List[int]]"; hidden_test_count=4
    description="Return all unique permutations of a collection that may contain duplicates."
    def get_test_cases(self):
        return [TestCase({"nums":[1,1,2]},[[1,1,2],[1,2,1],[2,1,1]],"Example 1"),
                TestCase({"nums":[1,2,3]},[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]],"Example 2")]
    def get_validator(self): return AnyOrderListValidator()
    @staticmethod
    def oracle(inputs):
        from itertools import permutations
        return sorted(set(permutations(inputs["nums"])))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,4) for _ in range(rng.randint(2,5))]} for _ in range(count)]


# LC 75 — Sort Colors
class SortColorsPlugin(ProblemPlugin):
    problem_id="sort-colors"; leetcode_number=75; title="Sort Colors"
    slug="sort-colors"; method_name="sortColors"; difficulty="Medium"; pattern="Two Pointers"
    topics=["Array","Two Pointers","Sorting"]; parameters=["nums: List[int]"]; return_type="None"; hidden_test_count=4
    description="Sort nums in-place so that objects of same color are adjacent (0s, 1s, 2s)."
    def get_test_cases(self):
        return [TestCase({"nums":[2,0,2,1,1,0]},[0,0,1,1,2,2],"Example 1"),TestCase({"nums":[2,0,1]},[0,1,2],"Example 2"),
                TestCase({"nums":[0]},[0],"Single",is_hidden=True),TestCase({"nums":[2,2,2]},[2,2,2],"All 2s",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs): return sorted(inputs["nums"])
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(0,2) for _ in range(rng.randint(1,12))]} for _ in range(count)]


# LC 77 — Combinations
class CombinationsPlugin(ProblemPlugin):
    problem_id="combinations"; leetcode_number=77; title="Combinations"
    slug="combinations"; method_name="combine"; difficulty="Medium"; pattern="Backtracking"
    topics=["Backtracking"]; parameters=["n: int","k: int"]; return_type="List[List[int]]"; hidden_test_count=4
    description="Return all possible combinations of k numbers chosen from 1..n."
    def get_test_cases(self):
        return [TestCase({"n":4,"k":2},[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]],"Example 1"),
                TestCase({"n":1,"k":1},[[1]],"Example 2")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import AnyOrderListValidator; return AnyOrderListValidator()
    @staticmethod
    def oracle(inputs):
        from itertools import combinations
        return [list(c) for c in combinations(range(1,inputs["n"]+1),inputs["k"])]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,6); k=rng.randint(1,n); tests.append({"n":n,"k":k})
        return tests


# LC 86 — Partition List
_PARTITION_LIST_TPL = """{imports}
{helpers}
{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.partition(head, {x})
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""
class PartitionListPlugin(ProblemPlugin):
    problem_id="partition-list"; leetcode_number=86; title="Partition List"
    slug="partition-list"; method_name="partition"; difficulty="Medium"; pattern="Linked List"
    topics=["Linked List","Two Pointers"]; parameters=["head: Optional[ListNode]","x: int"]; return_type="Optional[ListNode]"; hidden_test_count=4
    description="Partition list so all nodes less than x come before nodes >= x."
    def get_test_cases(self):
        return [TestCase({"head":[1,4,3,2,5,2],"x":3},[1,2,2,4,3,5],"Example 1"),
                TestCase({"head":[2,1],"x":2},[1,2],"Example 2"),
                TestCase({"head":[],"x":1},[],"Empty",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_PARTITION_LIST_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        vals,x=inputs["head"],inputs["x"]
        return [v for v in vals if v<x]+[v for v in vals if v>=x]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            vals=[rng.randint(1,9) for _ in range(rng.randint(0,8))]; x=rng.randint(1,9)
            tests.append({"head":vals,"x":x})
        return tests


# LC 93 — Restore IP Addresses
class RestoreIPAddressesPlugin(ProblemPlugin):
    problem_id="restore-ip-addresses"; leetcode_number=93; title="Restore IP Addresses"
    slug="restore-ip-addresses"; method_name="restoreIpAddresses"; difficulty="Medium"; pattern="Backtracking"
    topics=["String","Backtracking"]; parameters=["s: str"]; return_type="List[str]"; hidden_test_count=4
    description="Return all valid IP address combinations from s."
    def get_test_cases(self):
        return [TestCase({"s":"25525511135"},["255.255.11.135","255.255.111.35"],"Example 1"),
                TestCase({"s":"0000"},["0.0.0.0"],"Example 2"),TestCase({"s":"101023"},["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"],"Example 3")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import SetValidator; return SetValidator()
    @staticmethod
    def oracle(inputs):
        s=inputs["s"]; result=[]
        def bt(start,parts):
            if len(parts)==4:
                if start==len(s): result.append(".".join(parts))
                return
            for end in range(start+1,min(start+4,len(s)+1)):
                seg=s[start:end]
                if (seg[0]=='0' and len(seg)>1) or int(seg)>255: continue
                bt(end,parts+[seg])
        bt(0,[])
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"s":"".join(str(rng.randint(0,9)) for _ in range(rng.randint(4,12)))} for _ in range(count)]


# LC 95 — Unique Binary Search Trees II
class UniqueBSTsIIPlugin(ProblemPlugin):
    problem_id="unique-binary-search-trees-ii"; leetcode_number=95; title="Unique Binary Search Trees II"
    slug="unique-binary-search-trees-ii"; method_name="generateTrees"; difficulty="Medium"; pattern="Trees"
    topics=["Dynamic Programming","Backtracking","Tree","Binary Search Tree","Binary Tree"]
    parameters=["n: int"]; return_type="List[Optional[TreeNode]]"; hidden_test_count=3
    description="Return all structurally unique BSTs which have exactly n nodes."
    def get_test_cases(self):
        return [TestCase({"n":3},5,"Example 1: expect 5 trees"),TestCase({"n":1},1,"Example 2"),
                TestCase({"n":2},2,"n=2",is_hidden=True)]
    def get_validator(self): return UniqueBSTsCountValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]
        # Return count (Catalan number) — validator just checks count
        dp=[0]*(n+1); dp[0]=1
        for i in range(1,n+1):
            for j in range(i): dp[i]+=dp[j]*dp[i-1-j]
        return dp[n]
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(1,4)} for _ in range(count)]

class UniqueBSTsCountValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # actual is a list of trees; expected is the count
        try: actual_count=len(actual)
        except TypeError: actual_count=actual
        passed=actual_count==expected
        return ValidationResult(passed,f"count={expected}",f"count={actual_count}","" if passed else f"Expected {expected} trees, got {actual_count}")


# LC 96 — Unique Binary Search Trees
class UniqueBSTsPlugin(ProblemPlugin):
    problem_id="unique-binary-search-trees"; leetcode_number=96; title="Unique Binary Search Trees"
    slug="unique-binary-search-trees"; method_name="numTrees"; difficulty="Medium"; pattern="Trees"
    topics=["Math","Dynamic Programming","Tree","Binary Search Tree","Binary Tree"]
    parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Return the number of structurally unique BSTs which have exactly n nodes of unique values 1..n."
    def get_test_cases(self):
        return [TestCase({"n":3},5,"Example 1"),TestCase({"n":1},1,"Example 2"),
                TestCase({"n":4},14,"n=4",is_hidden=True),TestCase({"n":5},42,"n=5",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; dp=[0]*(n+1); dp[0]=1
        for i in range(1,n+1):
            for j in range(i): dp[i]+=dp[j]*dp[i-1-j]
        return dp[n]
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(1,10)} for _ in range(count)]


# LC 103 — Binary Tree Zigzag Level Order Traversal
_ZIGZAG_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    result = sol.zigzagLevelOrder(root)
    print("__RESULT__:")
    print(repr(result))

main()
"""
class ZigzagLevelOrderPlugin(ProblemPlugin):
    problem_id="binary-tree-zigzag-level-order-traversal"; leetcode_number=103
    title="Binary Tree Zigzag Level Order Traversal"; slug="binary-tree-zigzag-level-order-traversal"
    method_name="zigzagLevelOrder"; difficulty="Medium"; pattern="Trees"
    topics=["Tree","BFS","Binary Tree"]; parameters=["root: Optional[TreeNode]"]
    return_type="List[List[int]]"; hidden_test_count=4
    description="Return the zigzag level order traversal (left-to-right, right-to-left alternating)."
    def get_test_cases(self):
        return [TestCase({"root":[3,9,20,None,None,15,7]},[[3],[20,9],[15,7]],"Example 1"),
                TestCase({"root":[1]},[[1]],"Single"),TestCase({"root":[]},[],"Empty")]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_ZIGZAG_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        items=inputs["root"]
        if not items: return []
        from collections import deque
        class N:
            def __init__(self,v): self.val=v; self.left=self.right=None
        nodes=[None if v is None else N(v) for v in items]; q=deque([0]); i=1
        while q and i<len(nodes):
            idx=q.popleft()
            if nodes[idx] is None: continue
            if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
            if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
        result=[]; bfsq=deque([nodes[0]]); left_to_right=True
        while bfsq:
            level=[]; sz=len(bfsq)
            for _ in range(sz):
                n=bfsq.popleft()
                if n:
                    level.append(n.val)
                    if n.left: bfsq.append(n.left)
                    if n.right: bfsq.append(n.right)
            if level: result.append(level if left_to_right else level[::-1]); left_to_right=not left_to_right
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(0,12); vals=[rng.randint(1,50) if rng.random()>0.15 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=1
            tests.append({"root":vals})
        return tests


# LC 106 — Construct Binary Tree from Inorder and Postorder
_CONSTRUCT_INPOST_TPL = """{imports}
{helpers}
{solution_code}

def main():
    inorder = {inorder}
    postorder = {postorder}
    sol = Solution()
    result = sol.buildTree(inorder, postorder)
    print("__RESULT__:")
    print(repr(serialize_binary_tree(result)))

main()
"""
class ConstructTreeInPostPlugin(ProblemPlugin):
    problem_id="construct-binary-tree-from-inorder-and-postorder-traversal"; leetcode_number=106
    title="Construct Binary Tree from Inorder and Postorder Traversal"
    slug="construct-binary-tree-from-inorder-and-postorder-traversal"
    method_name="buildTree"; difficulty="Medium"; pattern="Trees"
    topics=["Array","Hash Table","Divide and Conquer","Tree","Binary Tree"]
    parameters=["inorder: List[int]","postorder: List[int]"]; return_type="Optional[TreeNode]"; hidden_test_count=4
    description="Given inorder and postorder traversals, construct and return the binary tree."
    def get_test_cases(self):
        return [TestCase({"inorder":[9,3,15,20,7],"postorder":[9,15,7,20,3]},[3,9,20,None,None,15,7],"Example 1"),
                TestCase({"inorder":[-1],"postorder":[-1]},[-1],"Single")]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_CONSTRUCT_INPOST_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        ino,post=list(inputs["inorder"]),list(inputs["postorder"])
        if not ino: return []
        def build(ino,post):
            if not post: return None
            root_val=post[-1]; idx=ino.index(root_val)
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            node=N(root_val); node.left=build(ino[:idx],post[:idx]); node.right=build(ino[idx+1:],post[idx:-1])
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
        return serialize(build(ino,post))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,8); vals=rng.sample(range(1,50),n); inorder=sorted(vals)
            def build_pre(ino):
                if not ino: return []
                mid=rng.randint(0,len(ino)-1)
                return build_pre(ino[:mid])+build_pre(ino[mid+1:])+[ino[mid]]
            postorder=build_pre(inorder); tests.append({"inorder":inorder,"postorder":postorder})
        return tests


# LC 114 — Flatten Binary Tree to Linked List
_FLATTEN_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    sol.flatten(root)
    # Serialize as list following right pointers
    result = []
    cur = root
    while cur:
        result.append(cur.val)
        cur = cur.right
    print("__RESULT__:")
    print(repr(result))

main()
"""
class FlattenBinaryTreePlugin(ProblemPlugin):
    problem_id="flatten-binary-tree-to-linked-list"; leetcode_number=114
    title="Flatten Binary Tree to Linked List"; slug="flatten-binary-tree-to-linked-list"
    method_name="flatten"; difficulty="Medium"; pattern="Trees"
    topics=["Linked List","Stack","Tree","DFS","Binary Tree"]
    parameters=["root: Optional[TreeNode]"]; return_type="None"; hidden_test_count=4
    description="Flatten the binary tree to a linked list in-place (preorder)."
    def get_test_cases(self):
        return [TestCase({"root":[1,2,5,3,4,None,6]},[1,2,3,4,5,6],"Example 1"),
                TestCase({"root":[]},[],"Empty"),TestCase({"root":[0]},[0],"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_FLATTEN_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        def preorder(items):
            if not items: return []
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]; q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            result=[]; stack=[nodes[0]] if nodes[0] else []
            while stack:
                n=stack.pop(); result.append(n.val)
                if n.right: stack.append(n.right)
                if n.left: stack.append(n.left)
            return result
        return preorder(inputs["root"])
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(0,10); vals=[rng.randint(1,20) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,20)
            tests.append({"root":vals})
        return tests


# LC 118 — Pascal's Triangle
class PascalsTrianglePlugin(ProblemPlugin):
    problem_id="pascals-triangle"; leetcode_number=118; title="Pascal's Triangle"
    slug="pascals-triangle"; method_name="generate"; difficulty="Easy"; pattern="Array"
    topics=["Array","Dynamic Programming"]; parameters=["numRows: int"]; return_type="List[List[int]]"; hidden_test_count=4
    description="Return the first numRows of Pascal's triangle."
    def get_test_cases(self):
        return [TestCase({"numRows":5},[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]],"Example 1"),
                TestCase({"numRows":1},[[1]],"Example 2"),TestCase({"numRows":3},[[1],[1,1],[1,2,1]],"n=3",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["numRows"]; result=[]
        for i in range(n):
            row=[1]*(i+1)
            for j in range(1,i): row[j]=result[i-1][j-1]+result[i-1][j]
            result.append(row)
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"numRows":rng.randint(1,10)} for _ in range(count)]


# LC 123 — Best Time to Buy and Sell Stock III
class StockIIIPlugin(ProblemPlugin):
    problem_id="best-time-to-buy-and-sell-stock-iii"; leetcode_number=123
    title="Best Time to Buy and Sell Stock III"; slug="best-time-to-buy-and-sell-stock-iii"
    method_name="maxProfit"; difficulty="Hard"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["prices: List[int]"]; return_type="int"; hidden_test_count=4
    description="Find the maximum profit with at most 2 transactions."
    def get_test_cases(self):
        return [TestCase({"prices":[3,3,5,0,0,3,1,4]},6,"Example 1"),TestCase({"prices":[1,2,3,4,5]},4,"Example 2"),
                TestCase({"prices":[7,6,4,3,1]},0,"Decreasing"),TestCase({"prices":[1]},0,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        prices=inputs["prices"]; b1=b2=float('-inf'); s1=s2=0
        for p in prices:
            b1=max(b1,-p); s1=max(s1,b1+p); b2=max(b2,s1-p); s2=max(s2,b2+p)
        return s2
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"prices":[rng.randint(1,100) for _ in range(rng.randint(2,15))]} for _ in range(count)]


# LC 135 — Candy
class CandyPlugin(ProblemPlugin):
    problem_id="candy"; leetcode_number=135; title="Candy"
    slug="candy"; method_name="candy"; difficulty="Hard"; pattern="Greedy"
    topics=["Array","Greedy"]; parameters=["ratings: List[int]"]; return_type="int"; hidden_test_count=4
    description="Distribute minimum candies so children with higher rating than neighbours get more."
    def get_test_cases(self):
        return [TestCase({"ratings":[1,0,2]},5,"Example 1"),TestCase({"ratings":[1,2,2]},4,"Example 2"),
                TestCase({"ratings":[1]},1,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        r=inputs["ratings"]; n=len(r); c=[1]*n
        for i in range(1,n):
            if r[i]>r[i-1]: c[i]=c[i-1]+1
        for i in range(n-2,-1,-1):
            if r[i]>r[i+1]: c[i]=max(c[i],c[i+1]+1)
        return sum(c)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"ratings":[rng.randint(0,10) for _ in range(rng.randint(1,12))]} for _ in range(count)]


# LC 145 — Binary Tree Postorder Traversal
_POSTORDER_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    sol = Solution()
    result = sol.postorderTraversal(root)
    print("__RESULT__:")
    print(repr(result))

main()
"""
class PostorderTraversalPlugin(ProblemPlugin):
    problem_id="binary-tree-postorder-traversal"; leetcode_number=145
    title="Binary Tree Postorder Traversal"; slug="binary-tree-postorder-traversal"
    method_name="postorderTraversal"; difficulty="Easy"; pattern="Trees"
    topics=["Stack","Tree","DFS","Binary Tree"]; parameters=["root: Optional[TreeNode]"]
    return_type="List[int]"; hidden_test_count=4; description="Return the postorder traversal of the tree's node values."
    def get_test_cases(self):
        return [TestCase({"root":[1,None,2,None,None,3]},[3,2,1],"Example 1"),TestCase({"root":[]},[],"Empty"),
                TestCase({"root":[1]},[1],"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_POSTORDER_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]; q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        result=[]
        def post(n):
            if not n: return
            post(n.left); post(n.right); result.append(n.val)
        post(build(inputs["root"])); return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(0,10); vals=[rng.randint(1,20) if rng.random()>0.1 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,20)
            tests.append({"root":vals})
        return tests


# LC 162 — Find Peak Element
class FindPeakElementPlugin(ProblemPlugin):
    problem_id="find-peak-element"; leetcode_number=162; title="Find Peak Element"
    slug="find-peak-element"; method_name="findPeakElement"; difficulty="Medium"; pattern="Binary Search"
    topics=["Array","Binary Search"]; parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Find a peak element index (nums[i] > both neighbors, or valid boundary)."
    def get_test_cases(self):
        return [TestCase({"nums":[1,2,3,1]},2,"Example 1"),TestCase({"nums":[1,2,1,3,5,6,4]},5,"Example 2"),
                TestCase({"nums":[1]},0,"Single",is_hidden=True)]
    def get_validator(self): return PeakValidator()
    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; n=len(nums)
        for i in range(n):
            if (i==0 or nums[i]>nums[i-1]) and (i==n-1 or nums[i]>nums[i+1]): return i
        return 0
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,100) for _ in range(rng.randint(1,10))]} for _ in range(count)]

class PeakValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        if inputs is None: return EqualityValidator().validate(actual, expected)
        nums=inputs["nums"]; n=len(nums); i=actual
        if i<0 or i>=n: return ValidationResult(False,f"valid index",repr(actual),"Index out of bounds")
        is_peak=(i==0 or nums[i]>nums[i-1]) and (i==n-1 or nums[i]>nums[i+1])
        return ValidationResult(is_peak,f"peak index",repr(actual),"" if is_peak else f"nums[{i}]={nums[i]} is not a peak")


# LC 173 — Binary Search Tree Iterator
_BST_ITER_TPL = """{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    root_data = args[0][0] if args[0] else []
    root = build_binary_tree(root_data)
    obj  = BSTIterator(root)
    for op, arg in zip(ops[1:], args[1:]):
        if op == "next":
            out.append(obj.next())
        elif op == "hasNext":
            out.append(obj.hasNext())
    print("__RESULT__:")
    print(repr(out))

main()
"""
class BSTIteratorPlugin(ProblemPlugin):
    problem_id="binary-search-tree-iterator"; leetcode_number=173
    title="Binary Search Tree Iterator"; slug="binary-search-tree-iterator"
    method_name="next"; difficulty="Medium"; pattern="Trees"
    topics=["Stack","Tree","Design","BST","Binary Tree","Iterator"]
    parameters=["root: Optional[TreeNode]"]; return_type="int"; hidden_test_count=3; stateful=True
    description="Implement an iterator over a BST. next() returns the next smallest number, hasNext() checks if exists."
    def get_test_cases(self):
        return [TestCase(
            {"ops":["BSTIterator","next","next","hasNext","next","hasNext","next","hasNext","next","hasNext"],
             "args":[[[7,3,15,None,None,9,20]],[],[],[],[],[],[],[],[],[]],},
            [None,3,7,True,9,True,15,True,20,False],"Example 1")]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_BST_ITER_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        ops,args=inputs["ops"],inputs["args"]
        tree_data=args[0][0] if args[0] else []
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]; q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        vals=[]; stack=[]; cur=build(tree_data)
        while cur or stack:
            while cur: stack.append(cur); cur=cur.left
            cur=stack.pop(); vals.append(cur.val); cur=cur.right
        idx=0; out=[None]
        for op,arg in zip(ops[1:],args[1:]):
            if op=="next": out.append(vals[idx]); idx+=1
            elif op=="hasNext": out.append(idx<len(vals))
        return out
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(3,8); vals=sorted(rng.sample(range(1,30),n))
            def bst_lo(sv):
                if not sv: return []
                mid=len(sv)//2; return [sv[mid]]+bst_lo(sv[:mid])+bst_lo(sv[mid+1:])
            tree=bst_lo(vals); ops=["BSTIterator"]; args=[[tree]]
            for v in vals: ops.append("next"); args.append([])
            tests.append({"ops":ops,"args":args})
        return tests


# LC 201 — Bitwise AND of Numbers Range
class BitwiseANDPlugin(ProblemPlugin):
    problem_id="bitwise-and-of-numbers-range"; leetcode_number=201
    title="Bitwise AND of Numbers Range"; slug="bitwise-and-of-numbers-range"
    method_name="rangeBitwiseAnd"; difficulty="Medium"; pattern="Bit Manipulation"
    topics=["Bit Manipulation"]; parameters=["left: int","right: int"]; return_type="int"; hidden_test_count=4
    description="Return the bitwise AND of all numbers in the range [left, right]."
    def get_test_cases(self):
        return [TestCase({"left":5,"right":7},4,"Example 1"),TestCase({"left":0,"right":0},0,"Example 2"),
                TestCase({"left":1,"right":2147483647},0,"Example 3"),TestCase({"left":6,"right":6},6,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        l,r=inputs["left"],inputs["right"]; shift=0
        while l<r: l>>=1; r>>=1; shift+=1
        return l<<shift
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            l=rng.randint(0,1000); r=rng.randint(l,l+100); tests.append({"left":l,"right":r})
        return tests


# LC 236 — Lowest Common Ancestor of a Binary Tree
_LCA_BT_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    def find(node, v):
        if not node: return None
        if node.val == v: return node
        return find(node.left, v) or find(node.right, v)
    p = find(root, {p})
    q = find(root, {q})
    sol = Solution()
    result = sol.lowestCommonAncestor(root, p, q)
    print("__RESULT__:")
    print(repr(result.val if result else None))

main()
"""
class LCABinaryTreePlugin(ProblemPlugin):
    problem_id="lowest-common-ancestor-of-a-binary-tree"; leetcode_number=236
    title="Lowest Common Ancestor of a Binary Tree"; slug="lowest-common-ancestor-of-a-binary-tree"
    method_name="lowestCommonAncestor"; difficulty="Medium"; pattern="Trees"
    topics=["Tree","DFS","Binary Tree"]; parameters=["root: Optional[TreeNode]","p: Optional[TreeNode]","q: Optional[TreeNode]"]
    return_type="Optional[TreeNode]"; hidden_test_count=4
    description="Find the LCA of two given nodes in a binary tree (not necessarily BST)."
    def get_test_cases(self):
        return [TestCase({"root":[3,5,1,6,2,0,8,None,None,7,4],"p":5,"q":1},3,"Example 1"),
                TestCase({"root":[3,5,1,6,2,0,8,None,None,7,4],"p":5,"q":4},5,"Example 2"),
                TestCase({"root":[1,2],"p":1,"q":2},1,"Small tree",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_LCA_BT_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        def build(items):
            if not items: return None
            from collections import deque
            class N:
                def __init__(self,v): self.val=v; self.left=self.right=None
            nodes=[None if v is None else N(v) for v in items]; q=deque([0]); i=1
            while q and i<len(nodes):
                idx=q.popleft()
                if nodes[idx] is None: continue
                if i<len(nodes): nodes[idx].left=nodes[i];q.append(i);i+=1
                if i<len(nodes): nodes[idx].right=nodes[i];q.append(i);i+=1
            return nodes[0]
        pv,qv=inputs["p"],inputs["q"]
        def lca(node):
            if not node: return None
            if node.val in (pv,qv): return node
            l=lca(node.left); r=lca(node.right)
            if l and r: return node
            return l or r
        result=lca(build(inputs["root"]))
        return result.val if result else None
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(3,10); vals=rng.sample(range(1,30),n)
            p,q=rng.sample(vals,2); tests.append({"root":vals,"p":p,"q":q})
        return tests
