"""Batch 6 — NeetCode 250: strings, arrays, graphs, trees, DP (problems ~160-185)."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, SetValidator, Validator, ValidationResult, AnyOrderListValidator
)
from backend.execution_engine.object_builder import LIST_NODE_HELPERS, TREE_NODE_HELPERS


# LC 344 — Reverse String
class ReverseStringPlugin(ProblemPlugin):
    problem_id="reverse-string"; leetcode_number=344; title="Reverse String"
    slug="reverse-string"; method_name="reverseString"; difficulty="Easy"; pattern="Two Pointers"
    topics=["Two Pointers","String"]; parameters=["s: List[str]"]; return_type="None"; hidden_test_count=4
    description="Reverse the input array of characters in-place."
    def get_test_cases(self):
        return [TestCase({"s":["h","e","l","l","o"]},["o","l","l","e","h"],"Example 1"),
                TestCase({"s":["H","a","n","n","a","h"]},["h","a","n","n","a","H"],"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs): return list(reversed(inputs["s"]))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; return [{"s":list(rng.choices(string.ascii_lowercase[:8],k=rng.randint(1,8)))} for _ in range(count)]


# LC 387 — First Unique Character in a String
class FirstUniqueCharPlugin(ProblemPlugin):
    problem_id="first-unique-character-in-a-string"; leetcode_number=387
    title="First Unique Character in a String"; slug="first-unique-character-in-a-string"
    method_name="firstUniqChar"; difficulty="Easy"; pattern="Array"
    topics=["Hash Table","String","Queue"]; parameters=["s: str"]; return_type="int"; hidden_test_count=4
    description="Return the index of the first non-repeating character, or -1 if it does not exist."
    def get_test_cases(self):
        return [TestCase({"s":"leetcode"},0,"Example 1"),TestCase({"s":"loveleetcode"},2,"Example 2"),
                TestCase({"s":"aabb"},-1,"Example 3"),TestCase({"s":"z"},0,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; s=inputs["s"]; cnt=Counter(s)
        for i,c in enumerate(s):
            if cnt[c]==1: return i
        return -1
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; return [{"s":"".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(1,12)))} for _ in range(count)]


# LC 242 already done. LC 28 — Find the Index of the First Occurrence in a String
class FindIndexFirstOccurrencePlugin(ProblemPlugin):
    problem_id="find-the-index-of-the-first-occurrence-in-a-string"; leetcode_number=28
    title="Find the Index of the First Occurrence in a String"
    slug="find-the-index-of-the-first-occurrence-in-a-string"
    method_name="strStr"; difficulty="Easy"; pattern="Array"
    topics=["Two Pointers","String","String Matching"]; parameters=["haystack: str","needle: str"]
    return_type="int"; hidden_test_count=4; description="Return the index of the first occurrence of needle in haystack, or -1."
    def get_test_cases(self):
        return [TestCase({"haystack":"sadbutsad","needle":"sad"},0,"Example 1"),
                TestCase({"haystack":"leetcode","needle":"leeto"},-1,"Example 2"),
                TestCase({"haystack":"a","needle":"a"},0,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs): return inputs["haystack"].find(inputs["needle"])
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for i in range(count):
            h="".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(5,12)))
            if i%2==0:
                start=rng.randint(0,max(0,len(h)-3)); n=h[start:start+rng.randint(1,3)]
            else: n="".join(rng.choices(string.ascii_lowercase[:6],k=2))
            tests.append({"haystack":h,"needle":n})
        return tests


# LC 125 already done. LC 26 — Remove Duplicates from Sorted Array
class RemoveDuplicatesSortedArrayPlugin(ProblemPlugin):
    problem_id="remove-duplicates-from-sorted-array"; leetcode_number=26
    title="Remove Duplicates from Sorted Array"; slug="remove-duplicates-from-sorted-array"
    method_name="removeDuplicates"; difficulty="Easy"; pattern="Two Pointers"
    topics=["Array","Two Pointers"]; parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Remove duplicates in-place and return the count of unique elements."
    def get_test_cases(self):
        return [TestCase({"nums":[1,1,2]},2,"Example 1"),TestCase({"nums":[0,0,1,1,1,2,2,3,3,4]},5,"Example 2"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs): return len(set(inputs["nums"]))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":sorted([rng.randint(1,10) for _ in range(rng.randint(1,12))])} for _ in range(count)]


# LC 80 — Remove Duplicates from Sorted Array II
class RemoveDuplicatesSortedArrayIIPlugin(ProblemPlugin):
    problem_id="remove-duplicates-from-sorted-array-ii"; leetcode_number=80
    title="Remove Duplicates from Sorted Array II"; slug="remove-duplicates-from-sorted-array-ii"
    method_name="removeDuplicates"; difficulty="Medium"; pattern="Two Pointers"
    topics=["Array","Two Pointers"]; parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Allow each element to appear at most twice; return the count."
    def get_test_cases(self):
        return [TestCase({"nums":[1,1,1,2,2,3]},5,"Example 1"),TestCase({"nums":[0,0,1,1,1,1,2,3,3]},7,"Example 2"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; cnt=Counter(inputs["nums"])
        return sum(min(v,2) for v in cnt.values())
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":sorted([rng.randint(1,8) for _ in range(rng.randint(2,15))])} for _ in range(count)]


# LC 189 — Rotate Array
class RotateArrayPlugin(ProblemPlugin):
    problem_id="rotate-array"; leetcode_number=189
    title="Rotate Array"; slug="rotate-array"; method_name="rotate"; difficulty="Medium"; pattern="Array"
    topics=["Array","Math","Two Pointers"]; parameters=["nums: List[int]","k: int"]
    return_type="None"; hidden_test_count=4; description="Rotate array to the right by k steps."
    def get_test_cases(self):
        return [TestCase({"nums":[1,2,3,4,5,6,7],"k":3},[5,6,7,1,2,3,4],"Example 1"),
                TestCase({"nums":[-1,-100,3,99],"k":2},[3,99,-1,-100],"Example 2"),
                TestCase({"nums":[1,2],"k":3},[2,1],"Overflow k",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums=list(inputs["nums"]); k=inputs["k"]%max(1,len(nums)); return nums[-k:]+nums[:-k] if k else nums
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(-50,50) for _ in range(rng.randint(2,10))],"k":rng.randint(0,15)} for _ in range(count)]


# LC 11 already done. LC 42 already done. LC 238 already done.
# LC 41 — First Missing Positive
class FirstMissingPositivePlugin(ProblemPlugin):
    problem_id="first-missing-positive"; leetcode_number=41
    title="First Missing Positive"; slug="first-missing-positive"
    method_name="firstMissingPositive"; difficulty="Hard"; pattern="Array"
    topics=["Array","Hash Table"]; parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Find the smallest missing positive integer."
    def get_test_cases(self):
        return [TestCase({"nums":[1,2,0]},3,"Example 1"),TestCase({"nums":[3,4,-1,1]},2,"Example 2"),
                TestCase({"nums":[7,8,9,11,12]},1,"Example 3"),TestCase({"nums":[1]},2,"Single 1",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s=set(inputs["nums"]); i=1
        while i in s: i+=1
        return i
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(-5,20) for _ in range(rng.randint(1,12))]} for _ in range(count)]


# LC 128 already done. LC 169 — Majority Element
class MajorityElementPlugin(ProblemPlugin):
    problem_id="majority-element"; leetcode_number=169
    title="Majority Element"; slug="majority-element"; method_name="majorityElement"
    difficulty="Easy"; pattern="Array"; topics=["Array","Hash Table","Divide and Conquer","Sorting","Counting"]
    parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Return the majority element (appears more than n/2 times)."
    def get_test_cases(self):
        return [TestCase({"nums":[3,2,3]},3,"Example 1"),TestCase({"nums":[2,2,1,1,1,2,2]},2,"Example 2"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; cnt=Counter(inputs["nums"]); return cnt.most_common(1)[0][0]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,10); maj=rng.randint(1,10)
            nums=[maj]*(n//2+1)+[rng.randint(1,10) for _ in range(n//2)]
            rng.shuffle(nums); tests.append({"nums":nums})
        return tests


# LC 229 — Majority Element II
class MajorityElementIIPlugin(ProblemPlugin):
    problem_id="majority-element-ii"; leetcode_number=229
    title="Majority Element II"; slug="majority-element-ii"; method_name="majorityElement"
    difficulty="Medium"; pattern="Array"; topics=["Array","Hash Table","Sorting","Counting"]
    parameters=["nums: List[int]"]; return_type="List[int]"; hidden_test_count=4
    description="Return all elements that appear more than n/3 times."
    def get_test_cases(self):
        return [TestCase({"nums":[3,2,3]},[3],"Example 1"),TestCase({"nums":[1]},[1],"Example 2"),
                TestCase({"nums":[1,2]},[1,2],"Example 3"),TestCase({"nums":[1,1,1,2,2,3]},[1,2],"Hidden",is_hidden=True)]
    def get_validator(self): return SetValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; nums=inputs["nums"]; n=len(nums)
        return sorted(k for k,v in Counter(nums).items() if v>n//3)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(3,12); nums=[rng.randint(1,5) for _ in range(n)]; tests.append({"nums":nums})
        return tests


# LC 274 — H-Index
class HIndexPlugin(ProblemPlugin):
    problem_id="h-index"; leetcode_number=274
    title="H-Index"; slug="h-index"; method_name="hIndex"; difficulty="Medium"; pattern="Array"
    topics=["Array","Sorting","Counting Sort"]; parameters=["citations: List[int]"]; return_type="int"; hidden_test_count=4
    description="Given citation counts for papers, return the h-index."
    def get_test_cases(self):
        return [TestCase({"citations":[3,0,6,1,5]},3,"Example 1"),TestCase({"citations":[1,3,1]},1,"Example 2"),
                TestCase({"citations":[0]},0,"All zero",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        citations=sorted(inputs["citations"],reverse=True)
        h=0
        for i,c in enumerate(citations):
            if c>=i+1: h=i+1
            else: break
        return h
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"citations":[rng.randint(0,10) for _ in range(rng.randint(1,8))]} for _ in range(count)]


# LC 380 — Insert Delete GetRandom O(1)
_RAND_SET_TPL = """{imports}
{helpers}
{solution_code}

def main():
    import random
    random.seed(42)
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = RandomizedSet()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "insert":
            out.append(obj.insert(arg[0]))
        elif op == "remove":
            out.append(obj.remove(arg[0]))
        elif op == "getRandom":
            out.append(obj.getRandom())
    print("__RESULT__:")
    print(repr(out))

main()
"""
class RandomizedSetPlugin(ProblemPlugin):
    problem_id="insert-delete-getrandom-o1"; leetcode_number=380
    title="Insert Delete GetRandom O(1)"; slug="insert-delete-getrandom-o1"
    method_name="insert"; difficulty="Medium"; pattern="Array"
    topics=["Array","Hash Table","Math","Design","Randomized"]; parameters=["val: int"]
    return_type="bool"; hidden_test_count=3; stateful=True
    description="Design a data structure with O(1) insert, remove, and getRandom."
    def get_test_cases(self):
        return [TestCase(
            {"ops":["RandomizedSet","insert","remove","insert","getRandom","remove","insert","getRandom"],
             "args":[[],[1],[2],[2],[],[1],[2],[]]},
            [None,True,False,True,2,True,False,2],"Example 1")]
    def get_validator(self): return RandomizedSetValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_RAND_SET_TPL)
    @staticmethod
    def oracle(inputs):
        ops,args=inputs["ops"],inputs["args"]; s=set(); out=[None]
        import random; random.seed(42)
        for op,arg in zip(ops[1:],args[1:]):
            if op=="insert":
                if arg[0] in s: out.append(False)
                else: s.add(arg[0]); out.append(True)
            elif op=="remove":
                if arg[0] not in s: out.append(False)
                else: s.remove(arg[0]); out.append(True)
            elif op=="getRandom": out.append(random.choice(list(s)))
        return out
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            ops=["RandomizedSet"]; args=[[]]
            vals=set()
            for _ in range(rng.randint(4,8)):
                op=rng.choice(["insert","remove"])
                v=rng.randint(1,6)
                ops.append(op); args.append([v])
                if rng.random()>0.5 and vals:
                    ops.append("getRandom"); args.append([])
            tests.append({"ops":ops,"args":args})
        return tests

class RandomizedSetValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # insert/remove results must match; getRandom just needs to be a valid int
        if len(actual)!=len(expected): return ValidationResult(False,repr(expected),repr(actual),"Length mismatch")
        for a,e in zip(actual,expected):
            if isinstance(e,bool):
                if a!=e: return ValidationResult(False,repr(expected),repr(actual),f"{a}!={e}")
            elif e is None:
                if a is not None: return ValidationResult(False,repr(expected),repr(actual),f"Expected None got {a}")
            # getRandom: just check it's an int
        return ValidationResult(True,repr(expected),repr(actual),"")


# LC 392 — Is Subsequence
class IsSubsequencePlugin(ProblemPlugin):
    problem_id="is-subsequence"; leetcode_number=392
    title="Is Subsequence"; slug="is-subsequence"; method_name="isSubsequence"
    difficulty="Easy"; pattern="Two Pointers"; topics=["Two Pointers","String","Dynamic Programming"]
    parameters=["s: str","t: str"]; return_type="bool"; hidden_test_count=4
    description="Return true if s is a subsequence of t."
    def get_test_cases(self):
        return [TestCase({"s":"abc","t":"ahbgdc"},True,"Example 1"),TestCase({"s":"axc","t":"ahbgdc"},False,"Example 2"),
                TestCase({"s":"","t":"abc"},True,"Empty s",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s,t=inputs["s"],inputs["t"]; i=0
        for c in t:
            if i<len(s) and c==s[i]: i+=1
        return i==len(s)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for i in range(count):
            t="".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(5,12)))
            if i%2==0: s="".join(rng.choices(t,k=rng.randint(0,4)))
            else: s="".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(1,4)))
            tests.append({"s":s,"t":t})
        return tests


# LC 443 — String Compression
class StringCompressionPlugin(ProblemPlugin):
    problem_id="string-compression"; leetcode_number=443
    title="String Compression"; slug="string-compression"; method_name="compress"
    difficulty="Medium"; pattern="Two Pointers"; topics=["Two Pointers","String"]
    parameters=["chars: List[str]"]; return_type="int"; hidden_test_count=4
    description="Compress chars in-place and return the new length."
    def get_test_cases(self):
        return [TestCase({"chars":["a","a","b","b","c","c","c"]},6,"Example 1"),
                TestCase({"chars":["a"]},1,"Example 2"),TestCase({"chars":["a","b","b","b","b","b","b","b","b","b","b","b","b"]},4,"Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        chars=list(inputs["chars"]); result=[]; i=0
        while i<len(chars):
            c=chars[i]; count=0
            while i<len(chars) and chars[i]==c: i+=1; count+=1
            result.append(c)
            if count>1: result.extend(list(str(count)))
        return len(result)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for _ in range(count):
            chars=[]
            for _ in range(rng.randint(1,5)):
                c=rng.choice(string.ascii_lowercase[:6]); chars.extend([c]*rng.randint(1,12))
            tests.append({"chars":chars})
        return tests


# LC 451 — Sort Characters By Frequency
class SortCharsByFrequencyPlugin(ProblemPlugin):
    problem_id="sort-characters-by-frequency"; leetcode_number=451
    title="Sort Characters By Frequency"; slug="sort-characters-by-frequency"
    method_name="frequencySort"; difficulty="Medium"; pattern="Hashing"
    topics=["Hash Table","String","Sorting","Heap","Bucket Sort"]
    parameters=["s: str"]; return_type="str"; hidden_test_count=4
    description="Sort characters in descending order of frequency."
    def get_test_cases(self):
        return [TestCase({"s":"tree"},"eert","Example 1"),TestCase({"s":"cccaaa"},"aaaccc","Example 2"),
                TestCase({"s":"Aabb"},"bbAa","Example 3")]
    def get_validator(self): return SortCharsByFreqValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; s=inputs["s"]; cnt=Counter(s)
        return "".join(c*n for c,n in cnt.most_common())
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; return [{"s":"".join(rng.choices(string.ascii_lowercase[:5],k=rng.randint(3,15)))} for _ in range(count)]

class SortCharsByFreqValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        from collections import Counter
        passed = Counter(actual)==Counter(expected)
        # Also verify descending freq
        if passed and actual:
            from collections import Counter as C2
            cnt=C2(actual); freqs=[cnt[c] for c in actual]
            for i in range(len(freqs)-1):
                if freqs[i]<freqs[i+1]: passed=False; break
        return ValidationResult(passed,repr(expected),repr(actual),"" if passed else "Frequency order wrong")


# LC 560 — Subarray Sum Equals K
class SubarraySumEqualsKPlugin(ProblemPlugin):
    problem_id="subarray-sum-equals-k"; leetcode_number=560
    title="Subarray Sum Equals K"; slug="subarray-sum-equals-k"
    method_name="subarraySum"; difficulty="Medium"; pattern="Hashing"
    topics=["Array","Hash Table","Prefix Sum"]
    parameters=["nums: List[int]","k: int"]; return_type="int"; hidden_test_count=4
    description="Return the total number of subarrays whose sum equals k."
    def get_test_cases(self):
        return [TestCase({"nums":[1,1,1],"k":2},2,"Example 1"),TestCase({"nums":[1,2,3],"k":3},2,"Example 2"),
                TestCase({"nums":[1],"k":1},1,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums,k=inputs["nums"],inputs["k"]; count=prefix=0; seen={0:1}
        for n in nums:
            prefix+=n; count+=seen.get(prefix-k,0); seen[prefix]=seen.get(prefix,0)+1
        return count
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(-5,5) for _ in range(rng.randint(2,15))],"k":rng.randint(-5,10)} for _ in range(count)]


# LC 209 — Minimum Size Subarray Sum
class MinSizeSubarraySumPlugin(ProblemPlugin):
    problem_id="minimum-size-subarray-sum"; leetcode_number=209
    title="Minimum Size Subarray Sum"; slug="minimum-size-subarray-sum"
    method_name="minSubArrayLen"; difficulty="Medium"; pattern="Sliding Window"
    topics=["Array","Binary Search","Sliding Window","Prefix Sum"]
    parameters=["target: int","nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Return the minimum length of a subarray whose sum >= target, or 0 if no such subarray."
    def get_test_cases(self):
        return [TestCase({"target":7,"nums":[2,3,1,2,4,3]},2,"Example 1"),
                TestCase({"target":4,"nums":[1,4,4]},1,"Example 2"),TestCase({"target":11,"nums":[1,1,1,1,1,1,1,1]},0,"Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        target,nums=inputs["target"],inputs["nums"]; l=total=0; best=float('inf')
        for r,n in enumerate(nums):
            total+=n
            while total>=target: best=min(best,r-l+1); total-=nums[l]; l+=1
        return best if best!=float('inf') else 0
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"target":rng.randint(3,20),"nums":[rng.randint(1,10) for _ in range(rng.randint(3,15))]} for _ in range(count)]
