"""Batch 8 — NeetCode 250: graphs, DP, linked lists, design (LC 23,25,32,44,240,260,261,264,278,297,343,355,374,402,406,452,455,502,523,525,605,632,721)."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, SetValidator, AnyOrderListValidator, Validator, ValidationResult
)
from backend.execution_engine.object_builder import LIST_NODE_HELPERS, TREE_NODE_HELPERS


# LC 23 — Merge k Sorted Lists
_MERGE_K_TPL = """{imports}
{helpers}
{solution_code}

def main():
    lists_data = {lists}
    lists = [build_linked_list(vals) for vals in lists_data]
    sol = Solution()
    result = sol.mergeKLists(lists)
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""
class MergeKSortedListsPlugin(ProblemPlugin):
    problem_id="merge-k-sorted-lists"; leetcode_number=23; title="Merge k Sorted Lists"
    slug="merge-k-sorted-lists"; method_name="mergeKLists"; difficulty="Hard"; pattern="Linked List"
    topics=["Linked List","Divide and Conquer","Heap","Merge Sort"]
    parameters=["lists: List[Optional[ListNode]]"]; return_type="Optional[ListNode]"; hidden_test_count=4
    description="Merge all k linked lists and return as one sorted list."
    def get_test_cases(self):
        return [TestCase({"lists":[[1,4,5],[1,3,4],[2,6]]},[1,1,2,3,4,4,5,6],"Example 1"),
                TestCase({"lists":[]},[],"Example 2"),TestCase({"lists":[[]]},[],"Example 3"),
                TestCase({"lists":[[1],[0]]},[0,1],"Two lists",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_MERGE_K_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        all_vals=[]
        for lst in inputs["lists"]: all_vals.extend(lst)
        return sorted(all_vals)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            k=rng.randint(2,5)
            tests.append({"lists":[sorted(rng.randint(1,20) for _ in range(rng.randint(0,6))) for _ in range(k)]})
        return tests


# LC 25 — Reverse Nodes in k-Group
_REVERSE_K_TPL = """{imports}
{helpers}
{solution_code}

def main():
    head = build_linked_list({head})
    sol = Solution()
    result = sol.reverseKGroup(head, {k})
    print("__RESULT__:")
    print(repr(serialize_linked_list(result)))

main()
"""
class ReverseKGroupPlugin(ProblemPlugin):
    problem_id="reverse-nodes-in-k-group"; leetcode_number=25; title="Reverse Nodes in k-Group"
    slug="reverse-nodes-in-k-group"; method_name="reverseKGroup"; difficulty="Hard"; pattern="Linked List"
    topics=["Linked List","Recursion"]; parameters=["head: Optional[ListNode]","k: int"]
    return_type="Optional[ListNode]"; hidden_test_count=4; description="Reverse nodes of list k at a time."
    def get_test_cases(self):
        return [TestCase({"head":[1,2,3,4,5],"k":2},[2,1,4,3,5],"Example 1"),
                TestCase({"head":[1,2,3,4,5],"k":3},[3,2,1,4,5],"Example 2"),
                TestCase({"head":[1,2,3],"k":1},[1,2,3],"k=1",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_REVERSE_K_TPL, helpers_str=LIST_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        vals=list(inputs["head"]); k=inputs["k"]; result=[]
        for i in range(0,len(vals),k):
            chunk=vals[i:i+k]
            result.extend(reversed(chunk) if len(chunk)==k else chunk)
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,10); vals=list(range(1,n+1)); k=rng.randint(1,n)
            tests.append({"head":vals,"k":k})
        return tests


# LC 32 — Longest Valid Parentheses
class LongestValidParenthesesPlugin(ProblemPlugin):
    problem_id="longest-valid-parentheses"; leetcode_number=32; title="Longest Valid Parentheses"
    slug="longest-valid-parentheses"; method_name="longestValidParentheses"; difficulty="Hard"; pattern="Stack"
    topics=["String","Dynamic Programming","Stack"]; parameters=["s: str"]; return_type="int"; hidden_test_count=4
    description="Return the length of the longest valid parentheses substring."
    def get_test_cases(self):
        return [TestCase({"s":"(()"},2,"Example 1"),TestCase({"s":")()())"},4,"Example 2"),
                TestCase({"s":""},0,"Empty"),TestCase({"s":"()(()"},4,"Mixed",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s=inputs["s"]; stack=[-1]; best=0
        for i,c in enumerate(s):
            if c=='(': stack.append(i)
            else:
                stack.pop()
                if not stack: stack.append(i)
                else: best=max(best,i-stack[-1])
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"s":"".join(rng.choices("()",k=rng.randint(2,14)))} for _ in range(count)]


# LC 44 — Wildcard Matching
class WildcardMatchingPlugin(ProblemPlugin):
    problem_id="wildcard-matching"; leetcode_number=44; title="Wildcard Matching"
    slug="wildcard-matching"; method_name="isMatch"; difficulty="Hard"; pattern="2-D DP"
    topics=["String","Dynamic Programming","Greedy","Recursion"]; parameters=["s: str","p: str"]
    return_type="bool"; hidden_test_count=4; description="Implement wildcard matching with '?' and '*'."
    def get_test_cases(self):
        return [TestCase({"s":"aa","p":"a"},False,"Example 1"),TestCase({"s":"aa","p":"*"},True,"Example 2"),
                TestCase({"s":"cb","p":"?a"},False,"Example 3"),TestCase({"s":"adceb","p":"*a*b"},True,"Example 4")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s,p=inputs["s"],inputs["p"]; m,n=len(s),len(p)
        dp=[[False]*(n+1) for _ in range(m+1)]; dp[0][0]=True
        for j in range(1,n+1):
            if p[j-1]=='*': dp[0][j]=dp[0][j-1]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if p[j-1]=='*': dp[i][j]=dp[i-1][j] or dp[i][j-1]
                elif p[j-1]=='?' or p[j-1]==s[i-1]: dp[i][j]=dp[i-1][j-1]
        return dp[m][n]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for i in range(count):
            s="".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(1,6)))
            if i%2==0:
                p="".join(rng.choices(list(string.ascii_lowercase[:4])+['*','?'],k=rng.randint(1,8)))
            else: p=s
            tests.append({"s":s,"p":p})
        return tests


# LC 240 — Search a 2D Matrix II
class SearchMatrix2DIIPlugin(ProblemPlugin):
    problem_id="search-a-2d-matrix-ii"; leetcode_number=240; title="Search a 2D Matrix II"
    slug="search-a-2d-matrix-ii"; method_name="searchMatrix"; difficulty="Medium"; pattern="Binary Search"
    topics=["Array","Binary Search","Divide and Conquer","Matrix"]
    parameters=["matrix: List[List[int]]","target: int"]; return_type="bool"; hidden_test_count=4
    description="Search target in m×n matrix where each row and column is sorted."
    def get_test_cases(self):
        return [TestCase({"matrix":[[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]],"target":5},True,"Example 1"),
                TestCase({"matrix":[[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]],"target":20},False,"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        m,t=inputs["matrix"],inputs["target"]
        if not m: return False
        rows,cols=len(m),len(m[0]); r,c=0,cols-1
        while r<rows and c>=0:
            if m[r][c]==t: return True
            elif m[r][c]>t: c-=1
            else: r+=1
        return False
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            rows,cols=rng.randint(2,5),rng.randint(2,5)
            flat=sorted(set(rng.randint(1,50) for _ in range(rows*cols*2)))[:rows*cols]
            matrix=[flat[r*cols:(r+1)*cols] for r in range(rows)]
            t=flat[rng.randint(0,len(flat)-1)] if i%2==0 else rng.randint(51,80)
            tests.append({"matrix":matrix,"target":t})
        return tests


# LC 260 — Single Number III
class SingleNumberIIIPlugin(ProblemPlugin):
    problem_id="single-number-iii"; leetcode_number=260; title="Single Number III"
    slug="single-number-iii"; method_name="singleNumber"; difficulty="Medium"; pattern="Bit Manipulation"
    topics=["Array","Bit Manipulation"]; parameters=["nums: List[int]"]; return_type="List[int]"; hidden_test_count=4
    description="Find two numbers appearing only once; return them in any order."
    def get_test_cases(self):
        return [TestCase({"nums":[1,2,1,3,2,5]},[3,5],"Example 1"),TestCase({"nums":[-1,0]},[-1,0],"Example 2")]
    def get_validator(self): return SetValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; cnt=Counter(inputs["nums"])
        return sorted(k for k,v in cnt.items() if v==1)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            a,b=rng.sample(range(1,20),2)
            pairs=[rng.randint(1,20) for _ in range(rng.randint(1,5))]
            nums=[a,b]+pairs+pairs; rng.shuffle(nums); tests.append({"nums":nums})
        return tests


# LC 261 — Graph Valid Tree
class GraphValidTreePlugin(ProblemPlugin):
    problem_id="graph-valid-tree"; leetcode_number=261; title="Graph Valid Tree"
    slug="graph-valid-tree"; method_name="validTree"; difficulty="Medium"; pattern="Graphs"
    topics=["DFS","BFS","Union Find","Graph"]; parameters=["n: int","edges: List[List[int]]"]
    return_type="bool"; hidden_test_count=4; description="Return true if n nodes and given edges form a valid tree."
    def get_test_cases(self):
        return [TestCase({"n":5,"edges":[[0,1],[0,2],[0,3],[1,4]]},True,"Example 1"),
                TestCase({"n":5,"edges":[[0,1],[1,2],[2,3],[1,3],[1,4]]},False,"Example 2"),
                TestCase({"n":1,"edges":[]},True,"Single node",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n,edges=inputs["n"],inputs["edges"]
        if len(edges)!=n-1: return False
        parent=list(range(n))
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        for u,v in edges:
            pu,pv=find(u),find(v)
            if pu==pv: return False
            parent[pu]=pv
        return True
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,7); edges=[[i,rng.randint(0,i-1)] for i in range(1,n)]
            tests.append({"n":n,"edges":edges})
        return tests


# LC 264 — Ugly Number II
class UglyNumberIIPlugin(ProblemPlugin):
    problem_id="ugly-number-ii"; leetcode_number=264; title="Ugly Number II"
    slug="ugly-number-ii"; method_name="nthUglyNumber"; difficulty="Medium"; pattern="Heap / Priority Queue"
    topics=["Hash Table","Math","Dynamic Programming","Heap"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Return the nth ugly number (positive integer whose prime factors are 2, 3, 5 only)."
    def get_test_cases(self):
        return [TestCase({"n":10},12,"Example 1"),TestCase({"n":1},1,"Example 2"),
                TestCase({"n":15},24,"n=15",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; ugly=[1]*n; i2=i3=i5=0
        for i in range(1,n):
            ugly[i]=min(ugly[i2]*2,ugly[i3]*3,ugly[i5]*5)
            if ugly[i]==ugly[i2]*2: i2+=1
            if ugly[i]==ugly[i3]*3: i3+=1
            if ugly[i]==ugly[i5]*5: i5+=1
        return ugly[n-1]
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(1,20)} for _ in range(count)]


# LC 278 — First Bad Version
_FIRST_BAD_TPL = """{imports}
{helpers}
{solution_code}

def main():
    n = {n}
    bad = {bad}
    # inject isBadVersion
    def isBadVersion(version):
        return version >= bad
    # patch into solution namespace
    import builtins
    builtins.isBadVersion = isBadVersion
    sol = Solution()
    result = sol.firstBadVersion(n)
    print("__RESULT__:")
    print(repr(result))

main()
"""
class FirstBadVersionPlugin(ProblemPlugin):
    problem_id="first-bad-version"; leetcode_number=278; title="First Bad Version"
    slug="first-bad-version"; method_name="firstBadVersion"; difficulty="Easy"; pattern="Binary Search"
    topics=["Binary Search","Interactive"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Find the first bad version using the isBadVersion API."
    def get_test_cases(self):
        return [TestCase({"n":5,"bad":4},4,"Example 1"),TestCase({"n":1,"bad":1},1,"Example 2"),
                TestCase({"n":10,"bad":1},1,"All bad",is_hidden=True),TestCase({"n":100,"bad":99},99,"Large",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_FIRST_BAD_TPL)
    @staticmethod
    def oracle(inputs): return inputs["bad"]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,1000); bad=rng.randint(1,n); tests.append({"n":n,"bad":bad})
        return tests


# LC 297 — Serialize and Deserialize Binary Tree
_SERIALIZE_TPL = """{imports}
{helpers}
{solution_code}

def main():
    root = build_binary_tree({root})
    codec = Codec()
    serialized = codec.serialize(root)
    deserialized = codec.deserialize(serialized)
    print("__RESULT__:")
    print(repr(serialize_binary_tree(deserialized)))

main()
"""
class SerializeDeserializeBinaryTreePlugin(ProblemPlugin):
    problem_id="serialize-and-deserialize-binary-tree"; leetcode_number=297
    title="Serialize and Deserialize Binary Tree"; slug="serialize-and-deserialize-binary-tree"
    method_name="serialize"; difficulty="Hard"; pattern="Trees"
    topics=["String","Tree","DFS","BFS","Design","Binary Tree"]
    parameters=["root: Optional[TreeNode]"]; return_type="str"; hidden_test_count=3
    description="Design an algorithm to serialize and deserialize a binary tree."
    def get_test_cases(self):
        return [TestCase({"root":[1,2,3,None,None,4,5]},[1,2,3,None,None,4,5],"Example 1"),
                TestCase({"root":[]},[],"Empty")]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_SERIALIZE_TPL, helpers_str=TREE_NODE_HELPERS)
    @staticmethod
    def oracle(inputs):
        vals=list(inputs["root"])
        while vals and vals[-1] is None: vals.pop()
        return vals
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(0,10); vals=[rng.randint(1,20) if rng.random()>0.15 else None for _ in range(n)]
            if vals and vals[0] is None: vals[0]=rng.randint(1,20)
            while vals and vals[-1] is None: vals.pop()
            tests.append({"root":vals})
        return tests


# LC 343 — Integer Break
class IntegerBreakPlugin(ProblemPlugin):
    problem_id="integer-break"; leetcode_number=343; title="Integer Break"
    slug="integer-break"; method_name="integerBreak"; difficulty="Medium"; pattern="1-D DP"
    topics=["Math","Dynamic Programming"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Break n into at least two positive integers that sum to n, maximizing their product."
    def get_test_cases(self):
        return [TestCase({"n":2},1,"Example 1"),TestCase({"n":10},36,"Example 2"),
                TestCase({"n":3},2,"n=3",is_hidden=True),TestCase({"n":6},9,"n=6",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; dp=[0]*(n+1); dp[1]=1
        for i in range(2,n+1):
            for j in range(1,i):
                dp[i]=max(dp[i],j*(i-j),j*dp[i-j])
        return dp[n]
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(2,15)} for _ in range(count)]


# LC 402 — Remove K Digits
class RemoveKDigitsPlugin(ProblemPlugin):
    problem_id="remove-k-digits"; leetcode_number=402; title="Remove K Digits"
    slug="remove-k-digits"; method_name="removeKdigits"; difficulty="Medium"; pattern="Greedy"
    topics=["String","Stack","Greedy","Monotonic Stack"]; parameters=["num: str","k: int"]; return_type="str"; hidden_test_count=4
    description="Remove k digits from num to make the resulting number smallest."
    def get_test_cases(self):
        return [TestCase({"num":"1432219","k":3},"1219","Example 1"),TestCase({"num":"10200","k":1},"200","Example 2"),
                TestCase({"num":"10","k":2},"0","Example 3"),TestCase({"num":"9","k":1},"0","Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        num,k=inputs["num"],inputs["k"]; stack=[]
        for d in num:
            while k and stack and stack[-1]>d: stack.pop(); k-=1
            stack.append(d)
        stack=stack[:-k] if k else stack
        return "".join(stack).lstrip('0') or "0"
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"num":str(rng.randint(100,99999)),"k":rng.randint(1,4)} for _ in range(count)]


# LC 406 — Queue Reconstruction by Height
class QueueReconstructionByHeightPlugin(ProblemPlugin):
    problem_id="queue-reconstruction-by-height"; leetcode_number=406
    title="Queue Reconstruction by Height"; slug="queue-reconstruction-by-height"
    method_name="reconstructQueue"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Binary Indexed Tree","Segment Tree","Sorting","Greedy"]
    parameters=["people: List[List[int]]"]; return_type="List[List[int]]"; hidden_test_count=4
    description="Reconstruct the queue: [h,k] means person of height h with k people of height >= h in front."
    def get_test_cases(self):
        return [TestCase({"people":[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]},[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]],"Example 1"),
                TestCase({"people":[[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]},[[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]],"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        people=sorted(inputs["people"],key=lambda x:(-x[0],x[1])); result=[]
        for p in people: result.insert(p[1],p)
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,8)
            people=[[rng.randint(1,10),rng.randint(0,3)] for _ in range(n)]; tests.append({"people":people})
        return tests


# LC 452 — Minimum Number of Arrows to Burst Balloons
class MinArrowsPlugin(ProblemPlugin):
    problem_id="minimum-number-of-arrows-to-burst-balloons"; leetcode_number=452
    title="Minimum Number of Arrows to Burst Balloons"; slug="minimum-number-of-arrows-to-burst-balloons"
    method_name="findMinArrowShots"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Greedy","Sorting"]; parameters=["points: List[List[int]]"]; return_type="int"; hidden_test_count=4
    description="Return the minimum arrows needed to burst all balloons."
    def get_test_cases(self):
        return [TestCase({"points":[[10,16],[2,8],[1,6],[7,12]]},2,"Example 1"),
                TestCase({"points":[[1,2],[3,4],[5,6],[7,8]]},4,"Example 2"),
                TestCase({"points":[[1,2],[2,3],[3,4],[4,5]]},2,"Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        pts=sorted(inputs["points"],key=lambda x:x[1]); arrows=1; end=pts[0][1]
        for s,e in pts[1:]:
            if s>end: arrows+=1; end=e
        return arrows
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,10)
            pts=[[rng.randint(0,20),(rng.randint(0,20))] for _ in range(n)]
            pts=[[min(a,b),max(a,b)] for a,b in pts]; tests.append({"points":pts})
        return tests


# LC 455 — Assign Cookies
class AssignCookiesPlugin(ProblemPlugin):
    problem_id="assign-cookies"; leetcode_number=455; title="Assign Cookies"
    slug="assign-cookies"; method_name="findContentChildren"; difficulty="Easy"; pattern="Greedy"
    topics=["Array","Two Pointers","Greedy","Sorting"]; parameters=["g: List[int]","s: List[int]"]
    return_type="int"; hidden_test_count=4; description="Maximize content children by assigning cookies greedily."
    def get_test_cases(self):
        return [TestCase({"g":[1,2,3],"s":[1,1]},1,"Example 1"),TestCase({"g":[1,2],"s":[1,2,3]},2,"Example 2"),
                TestCase({"g":[3],"s":[1,2]},0,"Not enough",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        g,s=sorted(inputs["g"]),sorted(inputs["s"]); i=j=0
        while i<len(g) and j<len(s):
            if s[j]>=g[i]: i+=1
            j+=1
        return i
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"g":[rng.randint(1,10) for _ in range(rng.randint(2,8))],"s":[rng.randint(1,10) for _ in range(rng.randint(2,8))]} for _ in range(count)]


# LC 523 — Continuous Subarray Sum
class ContinuousSubarraySumPlugin(ProblemPlugin):
    problem_id="continuous-subarray-sum"; leetcode_number=523
    title="Continuous Subarray Sum"; slug="continuous-subarray-sum"
    method_name="checkSubarraySum"; difficulty="Medium"; pattern="Hashing"
    topics=["Array","Hash Table","Math","Prefix Sum"]; parameters=["nums: List[int]","k: int"]
    return_type="bool"; hidden_test_count=4
    description="Return true if nums has a good subarray of length >= 2 whose sum is a multiple of k."
    def get_test_cases(self):
        return [TestCase({"nums":[23,2,4,6,7],"k":6},True,"Example 1"),TestCase({"nums":[23,2,6,4,7],"k":6},True,"Example 2"),
                TestCase({"nums":[23,2,6,4,7],"k":13},False,"Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums,k=inputs["nums"],inputs["k"]; seen={0:-1}; prefix=0
        for i,n in enumerate(nums):
            prefix=(prefix+n)%k
            if prefix in seen:
                if i-seen[prefix]>=2: return True
            else: seen[prefix]=i
        return False
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(0,20) for _ in range(rng.randint(2,10))],"k":rng.randint(2,10)} for _ in range(count)]


# LC 525 — Contiguous Array
class ContiguousArrayPlugin(ProblemPlugin):
    problem_id="contiguous-array"; leetcode_number=525; title="Contiguous Array"
    slug="contiguous-array"; method_name="findMaxLength"; difficulty="Medium"; pattern="Hashing"
    topics=["Array","Hash Table","Prefix Sum"]; parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Find maximum length subarray with equal number of 0s and 1s."
    def get_test_cases(self):
        return [TestCase({"nums":[0,1]},2,"Example 1"),TestCase({"nums":[0,1,0]},2,"Example 2"),
                TestCase({"nums":[0,0,1,0,0,0,1,1]},6,"Hidden",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; seen={0:-1}; best=prefix=0
        for i,n in enumerate(nums):
            prefix+=(1 if n else -1)
            if prefix in seen: best=max(best,i-seen[prefix])
            else: seen[prefix]=i
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(0,1) for _ in range(rng.randint(2,16))]} for _ in range(count)]


# LC 605 — Can Place Flowers
class CanPlaceFlowersPlugin(ProblemPlugin):
    problem_id="can-place-flowers"; leetcode_number=605; title="Can Place Flowers"
    slug="can-place-flowers"; method_name="canPlaceFlowers"; difficulty="Easy"; pattern="Greedy"
    topics=["Array","Greedy"]; parameters=["flowerbed: List[int]","n: int"]; return_type="bool"; hidden_test_count=4
    description="Return true if n new flowers can be planted without violating no-adjacent-flowers rule."
    def get_test_cases(self):
        return [TestCase({"flowerbed":[1,0,0,0,1],"n":1},True,"Example 1"),TestCase({"flowerbed":[1,0,0,0,1],"n":2},False,"Example 2"),
                TestCase({"flowerbed":[0],"n":1},True,"Single empty",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        bed=list(inputs["flowerbed"]); n=inputs["n"]; count=0
        for i in range(len(bed)):
            if bed[i]==0 and (i==0 or bed[i-1]==0) and (i==len(bed)-1 or bed[i+1]==0):
                bed[i]=1; count+=1
        return count>=n
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            bed=[rng.randint(0,1) for _ in range(rng.randint(2,12))]
            n=rng.randint(0,5); tests.append({"flowerbed":bed,"n":n})
        return tests


# LC 374 — Guess Number Higher or Lower
_GUESS_TPL = """{imports}
{helpers}
{solution_code}

def main():
    n = {n}
    pick = {pick}
    def guess(num):
        if num == pick: return 0
        return -1 if num > pick else 1
    import builtins
    builtins.guess = guess
    sol = Solution()
    result = sol.guessNumber(n)
    print("__RESULT__:")
    print(repr(result))

main()
"""
class GuessNumberPlugin(ProblemPlugin):
    problem_id="guess-number-higher-or-lower"; leetcode_number=374
    title="Guess Number Higher or Lower"; slug="guess-number-higher-or-lower"
    method_name="guessNumber"; difficulty="Easy"; pattern="Binary Search"
    topics=["Binary Search","Interactive"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Guess the number using the guess() API (returns -1/0/1)."
    def get_test_cases(self):
        return [TestCase({"n":10,"pick":6},6,"Example 1"),TestCase({"n":1,"pick":1},1,"Example 2"),
                TestCase({"n":2,"pick":1},1,"Example 3"),TestCase({"n":100,"pick":50},50,"Large",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_GUESS_TPL)
    @staticmethod
    def oracle(inputs): return inputs["pick"]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,1000); pick=rng.randint(1,n); tests.append({"n":n,"pick":pick})
        return tests


# LC 721 — Accounts Merge
class AccountsMergePlugin(ProblemPlugin):
    problem_id="accounts-merge"; leetcode_number=721; title="Accounts Merge"
    slug="accounts-merge"; method_name="accountsMerge"; difficulty="Medium"; pattern="Graphs"
    topics=["Array","Hash Table","String","DFS","BFS","Union Find"]
    parameters=["accounts: List[List[str]]"]; return_type="List[List[str]]"; hidden_test_count=3
    description="Merge accounts that share a common email. Each account is [name, email1, email2, ...]."
    def get_test_cases(self):
        return [TestCase({"accounts":[["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]},
                         [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]],"Example 1")]
    def get_validator(self): return AccountsMergeValidator()
    @staticmethod
    def oracle(inputs):
        from collections import defaultdict
        accounts=inputs["accounts"]
        email_to_name={}; graph=defaultdict(set)
        for acc in accounts:
            name=acc[0]
            for email in acc[1:]:
                email_to_name[email]=name
                graph[acc[1]].add(email); graph[email].add(acc[1])
        visited=set(); result=[]
        def dfs(email,component):
            if email in visited: return
            visited.add(email); component.append(email)
            for nb in graph[email]: dfs(nb,component)
        for email in email_to_name:
            if email not in visited:
                comp=[]; dfs(email,comp)
                result.append([email_to_name[comp[0]]]+sorted(comp))
        return sorted(result)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            shared="shared@x.com"
            tests.append({"accounts":[["Alice","alice@x.com",shared],["Bob","bob@x.com",shared],["Carol","carol@x.com"]]})
        return tests

class AccountsMergeValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        try:
            a=sorted([acc[0]]+sorted(acc[1:]) for acc in actual)
            e=sorted([acc[0]]+sorted(acc[1:]) for acc in expected)
            passed=a==e
        except Exception: passed=False; a,e=actual,expected
        return ValidationResult(passed,repr(e),repr(a),"" if passed else "Accounts differ")


# LC 502 — IPO
class IPOPlugin(ProblemPlugin):
    problem_id="ipo"; leetcode_number=502; title="IPO"
    slug="ipo"; method_name="findMaximizedCapital"; difficulty="Hard"; pattern="Greedy"
    topics=["Array","Greedy","Sorting","Heap"]; parameters=["k: int","w: int","profits: List[int]","capital: List[int]"]
    return_type="int"; hidden_test_count=4; description="Maximize capital by completing at most k projects."
    def get_test_cases(self):
        return [TestCase({"k":2,"w":0,"profits":[1,2,3],"capital":[0,1,1]},4,"Example 1"),
                TestCase({"k":3,"w":0,"profits":[1,2,3],"capital":[0,1,2]},6,"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        import heapq
        k,w,profits,capital=inputs["k"],inputs["w"],inputs["profits"],inputs["capital"]
        projects=sorted(zip(capital,profits)); i=0; available=[]
        for _ in range(k):
            while i<len(projects) and projects[i][0]<=w:
                heapq.heappush(available,-projects[i][1]); i+=1
            if not available: break
            w+=-heapq.heappop(available)
        return w
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,8); k=rng.randint(1,n)
            profits=[rng.randint(1,20) for _ in range(n)]
            capital=[rng.randint(0,10) for _ in range(n)]
            tests.append({"k":k,"w":rng.randint(0,5),"profits":profits,"capital":capital})
        return tests
