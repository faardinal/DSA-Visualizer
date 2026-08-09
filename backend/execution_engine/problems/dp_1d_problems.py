"""1-D Dynamic Programming pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator


# LC 70 — Climbing Stairs
class ClimbingStairsPlugin(ProblemPlugin):
    problem_id="climbing-stairs"; leetcode_number=70; title="Climbing Stairs"; slug="climbing-stairs"
    method_name="climbStairs"; difficulty="Easy"; pattern="1-D DP"
    topics=["Math","Dynamic Programming","Memoization"]; parameters=["n: int"]; return_type="int"
    hidden_test_count=4; description="Count ways to climb n stairs taking 1 or 2 steps at a time."

    def get_test_cases(self):
        return [TestCase({"n":2},2,"Example 1"),TestCase({"n":3},3,"Example 2"),
                TestCase({"n":1},1,"n=1",is_hidden=True),TestCase({"n":10},89,"n=10",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        n=inputs["n"]
        if n<=2: return n
        a,b=1,2
        for _ in range(3,n+1): a,b=b,a+b
        return b

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"n":rng.randint(1,30)} for _ in range(count)]


# LC 746 — Min Cost Climbing Stairs
class MinCostClimbingStairsPlugin(ProblemPlugin):
    problem_id="min-cost-climbing-stairs"; leetcode_number=746; title="Min Cost Climbing Stairs"
    slug="min-cost-climbing-stairs"; method_name="minCostClimbingStairs"; difficulty="Easy"
    pattern="1-D DP"; topics=["Array","Dynamic Programming"]; parameters=["cost: List[int]"]
    return_type="int"; hidden_test_count=4; description="Find min cost to reach top of floor."

    def get_test_cases(self):
        return [TestCase({"cost":[10,15,20]},15,"Example 1"),
                TestCase({"cost":[1,100,1,1,1,100,1,1,100,1]},6,"Example 2"),
                TestCase({"cost":[0,0]},0,"Zeros",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        cost=inputs["cost"]; n=len(cost)
        dp=[0]*(n+1)
        for i in range(2,n+1):
            dp[i]=min(dp[i-1]+cost[i-1],dp[i-2]+cost[i-2])
        return dp[n]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"cost":[rng.randint(0,100) for _ in range(rng.randint(2,15))]} for _ in range(count)]


# LC 198 — House Robber
class HouseRobberPlugin(ProblemPlugin):
    problem_id="house-robber"; leetcode_number=198; title="House Robber"; slug="house-robber"
    method_name="rob"; difficulty="Medium"; pattern="1-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["nums: List[int]"]; return_type="int"
    hidden_test_count=4; description="Max money without robbing adjacent houses."

    def get_test_cases(self):
        return [TestCase({"nums":[1,2,3,1]},4,"Example 1"),TestCase({"nums":[2,7,9,3,1]},12,"Example 2"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True),TestCase({"nums":[2,1]},2,"Two",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]
        if not nums: return 0
        if len(nums)==1: return nums[0]
        a,b=nums[0],max(nums[0],nums[1])
        for i in range(2,len(nums)): a,b=b,max(b,a+nums[i])
        return b

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,400) for _ in range(rng.randint(1,20))]} for _ in range(count)]


# LC 213 — House Robber II
class HouseRobberIIPlugin(ProblemPlugin):
    problem_id="house-robber-ii"; leetcode_number=213; title="House Robber II"; slug="house-robber-ii"
    method_name="rob"; difficulty="Medium"; pattern="1-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["nums: List[int]"]; return_type="int"
    hidden_test_count=4; description="House robber on a circular array."

    def get_test_cases(self):
        return [TestCase({"nums":[2,3,2]},3,"Example 1"),TestCase({"nums":[1,2,3,1]},4,"Example 2"),
                TestCase({"nums":[1,2,3]},3,"Three houses",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]
        def rob1(arr):
            if not arr: return 0
            if len(arr)==1: return arr[0]
            a,b=arr[0],max(arr[0],arr[1])
            for i in range(2,len(arr)): a,b=b,max(b,a+arr[i])
            return b
        if len(nums)==1: return nums[0]
        return max(rob1(nums[:-1]),rob1(nums[1:]))

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,400) for _ in range(rng.randint(2,20))]} for _ in range(count)]


# LC 5 — Longest Palindromic Substring
class LongestPalindromeSubstringPlugin(ProblemPlugin):
    problem_id="longest-palindromic-substring"; leetcode_number=5; title="Longest Palindromic Substring"
    slug="longest-palindromic-substring"; method_name="longestPalindrome"; difficulty="Medium"
    pattern="1-D DP"; topics=["String","Dynamic Programming"]; parameters=["s: str"]
    return_type="str"; hidden_test_count=4; description="Return the longest palindromic substring."

    def get_test_cases(self):
        return [TestCase({"s":"babad"},"bab","Example 1"),TestCase({"s":"cbbd"},"bb","Example 2"),
                TestCase({"s":"a"},"a","Single",is_hidden=True),TestCase({"s":"ac"},"a","Two",is_hidden=True)]

    def get_validator(self):
        return LongestPalindromeValidator()

    @staticmethod
    def oracle(inputs):
        s=inputs["s"]; best=""
        for i in range(len(s)):
            for l,r in [(i,i),(i,i+1)]:
                while l>=0 and r<len(s) and s[l]==s[r]: l-=1;r+=1
                if r-l-1>len(best): best=s[l+1:r]
        return best

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        tests=[]
        for i in range(count):
            if i%2==0:
                half=[rng.choice(string.ascii_lowercase[:6]) for _ in range(rng.randint(1,6))]
                s="".join(half+half[-2::-1])
            else:
                s="".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(2,12)))
            tests.append({"s":s})
        return tests

from backend.execution_engine.plugin_base import Validator, ValidationResult
class LongestPalindromeValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # Both must be palindromes of same length
        def is_pal(s): return s==s[::-1]
        passed = is_pal(str(actual)) and len(str(actual))==len(str(expected))
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected palindrome len {len(expected)}, got {repr(actual)}")


# LC 647 — Palindromic Substrings
class PalindromicSubstringsPlugin(ProblemPlugin):
    problem_id="palindromic-substrings"; leetcode_number=647; title="Palindromic Substrings"
    slug="palindromic-substrings"; method_name="countSubstrings"; difficulty="Medium"
    pattern="1-D DP"; topics=["String","Dynamic Programming"]; parameters=["s: str"]
    return_type="int"; hidden_test_count=4; description="Count the number of palindromic substrings."

    def get_test_cases(self):
        return [TestCase({"s":"abc"},3,"Example 1"),TestCase({"s":"aaa"},6,"Example 2"),
                TestCase({"s":"a"},1,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s=inputs["s"]; count=0
        for i in range(len(s)):
            for l,r in [(i,i),(i,i+1)]:
                while l>=0 and r<len(s) and s[l]==s[r]: count+=1;l-=1;r+=1
        return count

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        return [{"s":"".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(1,12)))} for _ in range(count)]


# LC 91 — Decode Ways
class DecodeWaysPlugin(ProblemPlugin):
    problem_id="decode-ways"; leetcode_number=91; title="Decode Ways"; slug="decode-ways"
    method_name="numDecodings"; difficulty="Medium"; pattern="1-D DP"
    topics=["String","Dynamic Programming"]; parameters=["s: str"]; return_type="int"
    hidden_test_count=4; description="Count number of ways to decode a numeric string (A=1…Z=26)."

    def get_test_cases(self):
        return [TestCase({"s":"12"},2,"Example 1"),TestCase({"s":"226"},3,"Example 2"),
                TestCase({"s":"06"},0,"Leading zero"),TestCase({"s":"10"},1,"10",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s=inputs["s"]
        if not s or s[0]=='0': return 0
        n=len(s); dp=[0]*(n+1); dp[0]=dp[1]=1
        for i in range(2,n+1):
            if s[i-1]!='0': dp[i]+=dp[i-1]
            two=int(s[i-2:i])
            if 10<=two<=26: dp[i]+=dp[i-2]
        return dp[n]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,8)
            s="".join(str(rng.randint(1,9)) if i==0 else str(rng.randint(0,9)) for i in range(n))
            tests.append({"s":s})
        return tests


# LC 139 — Word Break
class WordBreakPlugin(ProblemPlugin):
    problem_id="word-break"; leetcode_number=139; title="Word Break"; slug="word-break"
    method_name="wordBreak"; difficulty="Medium"; pattern="1-D DP"
    topics=["Hash Table","String","Dynamic Programming","Trie","Memoization"]
    parameters=["s: str","wordDict: List[str]"]; return_type="bool"
    hidden_test_count=4; description="Return true if s can be segmented into words from wordDict."

    def get_test_cases(self):
        return [TestCase({"s":"leetcode","wordDict":["leet","code"]},True,"Example 1"),
                TestCase({"s":"applepenapple","wordDict":["apple","pen"]},True,"Example 2"),
                TestCase({"s":"catsandog","wordDict":["cats","dog","sand","and","cat"]},False,"Example 3"),
                TestCase({"s":"a","wordDict":["b"]},False,"No match",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s,words=inputs["s"],set(inputs["wordDict"])
        dp=[False]*(len(s)+1); dp[0]=True
        for i in range(1,len(s)+1):
            for j in range(i):
                if dp[j] and s[j:i] in words: dp[i]=True; break
        return dp[len(s)]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            words=["cat","dog","pen","apple","sand","and","cats"]
            if i%2==0:
                import random
                s="".join(rng.choices(words,k=rng.randint(1,3)))
                tests.append({"s":s,"wordDict":words})
            else:
                tests.append({"s":"abcdef","wordDict":["ab","cd"]})
        return tests


# LC 300 — Longest Increasing Subsequence
class LongestIncreasingSubsequencePlugin(ProblemPlugin):
    problem_id="longest-increasing-subsequence"; leetcode_number=300; title="Longest Increasing Subsequence"
    slug="longest-increasing-subsequence"; method_name="lengthOfLIS"; difficulty="Medium"
    pattern="1-D DP"; topics=["Array","Binary Search","Dynamic Programming"]
    parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Return the length of the longest strictly increasing subsequence."

    def get_test_cases(self):
        return [TestCase({"nums":[10,9,2,5,3,7,101,18]},4,"Example 1"),
                TestCase({"nums":[0,1,0,3,2,3]},4,"Example 2"),
                TestCase({"nums":[7,7,7,7,7]},1,"All same"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]
        if not nums: return 0
        dp=[1]*len(nums)
        for i in range(len(nums)):
            for j in range(i): 
                if nums[j]<nums[i]: dp[i]=max(dp[i],dp[j]+1)
        return max(dp)

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(-50,50) for _ in range(rng.randint(1,20))]} for _ in range(count)]


# LC 1143 — Longest Common Subsequence
class LongestCommonSubsequencePlugin(ProblemPlugin):
    problem_id="longest-common-subsequence"; leetcode_number=1143; title="Longest Common Subsequence"
    slug="longest-common-subsequence"; method_name="longestCommonSubsequence"; difficulty="Medium"
    pattern="2-D DP"; topics=["String","Dynamic Programming"]
    parameters=["text1: str","text2: str"]; return_type="int"; hidden_test_count=4
    description="Return the length of the longest common subsequence of text1 and text2."

    def get_test_cases(self):
        return [TestCase({"text1":"abcde","text2":"ace"},3,"Example 1"),
                TestCase({"text1":"abc","text2":"abc"},3,"Example 2"),
                TestCase({"text1":"abc","text2":"def"},0,"Example 3"),
                TestCase({"text1":"a","text2":"b"},0,"No match",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        t1,t2=inputs["text1"],inputs["text2"]
        m,n=len(t1),len(t2)
        dp=[[0]*(n+1) for _ in range(m+1)]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if t1[i-1]==t2[j-1]: dp[i][j]=dp[i-1][j-1]+1
                else: dp[i][j]=max(dp[i-1][j],dp[i][j-1])
        return dp[m][n]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        return [{"text1":"".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(1,10))),
                 "text2":"".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(1,10)))} for _ in range(count)]
