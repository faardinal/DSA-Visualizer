"""Advanced DP, String DP, and remaining NeetCode 250 DP problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator, FloatValidator


# LC 322 — Coin Change
class CoinChangePlugin(ProblemPlugin):
    problem_id="coin-change"; leetcode_number=322; title="Coin Change"; slug="coin-change"
    method_name="coinChange"; difficulty="Medium"; pattern="1-D DP"
    topics=["Array","Dynamic Programming","BFS"]; parameters=["coins: List[int]","amount: int"]
    return_type="int"; hidden_test_count=4; description="Return fewest coins to make amount, or -1 if impossible."

    def get_test_cases(self):
        return [TestCase({"coins":[1,2,5],"amount":11},3,"Example 1"),
                TestCase({"coins":[2],"amount":3},-1,"Example 2"),
                TestCase({"coins":[1],"amount":0},0,"Zero amount"),
                TestCase({"coins":[1,2,5],"amount":100},20,"Large",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        coins,amount=inputs["coins"],inputs["amount"]
        dp=[float('inf')]*(amount+1); dp[0]=0
        for i in range(1,amount+1):
            for c in coins:
                if c<=i: dp[i]=min(dp[i],dp[i-c]+1)
        return dp[amount] if dp[amount]!=float('inf') else -1

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            coins=list(set(rng.randint(1,10) for _ in range(rng.randint(2,5))))
            amount=rng.randint(0,30)
            tests.append({"coins":coins,"amount":amount})
        return tests


# LC 152 — Maximum Product Subarray
class MaxProductSubarrayPlugin(ProblemPlugin):
    problem_id="maximum-product-subarray"; leetcode_number=152; title="Maximum Product Subarray"
    slug="maximum-product-subarray"; method_name="maxProduct"; difficulty="Medium"; pattern="1-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4; description="Find the subarray with the largest product and return the product."

    def get_test_cases(self):
        return [TestCase({"nums":[2,3,-2,4]},6,"Example 1"),
                TestCase({"nums":[-2,0,-1]},0,"Example 2"),
                TestCase({"nums":[-2]},-2,"Single negative"),
                TestCase({"nums":[2,-5,-2,-4,3]},24,"Hidden",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; best=cur_max=cur_min=nums[0]
        for n in nums[1:]:
            candidates=(n,cur_max*n,cur_min*n)
            cur_max,cur_min=max(candidates),min(candidates)
            best=max(best,cur_max)
        return best

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(-10,10) for _ in range(rng.randint(1,15))]} for _ in range(count)]


# LC 416 — Partition Equal Subset Sum
class PartitionEqualSubsetSumPlugin(ProblemPlugin):
    problem_id="partition-equal-subset-sum"; leetcode_number=416; title="Partition Equal Subset Sum"
    slug="partition-equal-subset-sum"; method_name="canPartition"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["nums: List[int]"]
    return_type="bool"; hidden_test_count=4; description="Return true if the array can be partitioned into two subsets with equal sum."

    def get_test_cases(self):
        return [TestCase({"nums":[1,5,11,5]},True,"Example 1"),
                TestCase({"nums":[1,2,3,5]},False,"Example 2"),
                TestCase({"nums":[1,1]},True,"Two equal",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; total=sum(nums)
        if total%2: return False
        target=total//2; dp={0}
        for n in nums:
            dp|={s+n for s in dp}
        return target in dp

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            if i%2==0:
                n=rng.randint(2,10); half=[rng.randint(1,10) for _ in range(n)]
                tests.append({"nums":half+half})
            else:
                tests.append({"nums":[rng.randint(1,10) for _ in range(rng.randint(3,10))]})
        return tests


# LC 115 — Distinct Subsequences
class DistinctSubsequencesPlugin(ProblemPlugin):
    problem_id="distinct-subsequences"; leetcode_number=115; title="Distinct Subsequences"
    slug="distinct-subsequences"; method_name="numDistinct"; difficulty="Hard"; pattern="2-D DP"
    topics=["String","Dynamic Programming"]; parameters=["s: str","t: str"]
    return_type="int"; hidden_test_count=4; description="Count distinct subsequences of s that equal t."

    def get_test_cases(self):
        return [TestCase({"s":"rabbbit","t":"rabbit"},3,"Example 1"),
                TestCase({"s":"babgbag","t":"bag"},5,"Example 2"),
                TestCase({"s":"a","t":"b"},0,"No match",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s,t=inputs["s"],inputs["t"]; m,n=len(s),len(t)
        dp=[[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0]=1
        for i in range(1,m+1):
            for j in range(1,n+1):
                dp[i][j]=dp[i-1][j]+(dp[i-1][j-1] if s[i-1]==t[j-1] else 0)
        return dp[m][n]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        return [{"s":"".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(4,10))),
                 "t":"".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(1,4)))} for _ in range(count)]


# LC 329 — Longest Increasing Path in a Matrix
class LongestIncreasingPathPlugin(ProblemPlugin):
    problem_id="longest-increasing-path-in-a-matrix"; leetcode_number=329
    title="Longest Increasing Path in a Matrix"; slug="longest-increasing-path-in-a-matrix"
    method_name="longestIncreasingPath"; difficulty="Hard"; pattern="2-D DP"
    topics=["Array","Dynamic Programming","DFS","BFS","Graph","Topological Sort","Memoization","Matrix"]
    parameters=["matrix: List[List[int]]"]; return_type="int"; hidden_test_count=4
    description="Return the length of the longest increasing path in the matrix."

    def get_test_cases(self):
        return [TestCase({"matrix":[[9,9,4],[6,6,8],[2,1,1]]},4,"Example 1"),
                TestCase({"matrix":[[3,4,5],[3,2,6],[2,2,1]]},4,"Example 2"),
                TestCase({"matrix":[[1]]},1,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        matrix=inputs["matrix"]
        if not matrix: return 0
        rows,cols=len(matrix),len(matrix[0])
        memo={}
        def dfs(r,c):
            if (r,c) in memo: return memo[(r,c)]
            best=1
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<rows and 0<=nc<cols and matrix[nr][nc]>matrix[r][c]:
                    best=max(best,1+dfs(nr,nc))
            memo[(r,c)]=best; return best
        return max(dfs(r,c) for r in range(rows) for c in range(cols))

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            r=rng.randint(2,5); c=rng.randint(2,5)
            tests.append({"matrix":[[rng.randint(1,20) for _ in range(c)] for _ in range(r)]})
        return tests


# LC 97 — Interleaving String
class InterleavingStringPlugin(ProblemPlugin):
    problem_id="interleaving-string"; leetcode_number=97; title="Interleaving String"
    slug="interleaving-string"; method_name="isInterleave"; difficulty="Medium"; pattern="2-D DP"
    topics=["String","Dynamic Programming"]; parameters=["s1: str","s2: str","s3: str"]
    return_type="bool"; hidden_test_count=4
    description="Return true if s3 is formed by interleaving s1 and s2."

    def get_test_cases(self):
        return [TestCase({"s1":"aabcc","s2":"dbbca","s3":"aadbbcbcac"},True,"Example 1"),
                TestCase({"s1":"aabcc","s2":"dbbca","s3":"aadbbbaccc"},False,"Example 2"),
                TestCase({"s1":"","s2":"","s3":""},True,"All empty",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s1,s2,s3=inputs["s1"],inputs["s2"],inputs["s3"]
        m,n=len(s1),len(s2)
        if m+n!=len(s3): return False
        dp=[[False]*(n+1) for _ in range(m+1)]; dp[0][0]=True
        for i in range(1,m+1): dp[i][0]=dp[i-1][0] and s1[i-1]==s3[i-1]
        for j in range(1,n+1): dp[0][j]=dp[0][j-1] and s2[j-1]==s3[j-1]
        for i in range(1,m+1):
            for j in range(1,n+1):
                dp[i][j]=(dp[i-1][j] and s1[i-1]==s3[i+j-1]) or (dp[i][j-1] and s2[j-1]==s3[i+j-1])
        return dp[m][n]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        tests=[]
        for i in range(count):
            s1="".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(1,5)))
            s2="".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(1,5)))
            if i%2==0:
                # valid interleave
                merged=[]; i1=i2=0
                while i1<len(s1) or i2<len(s2):
                    if i1<len(s1) and (i2>=len(s2) or rng.random()>0.5): merged.append(s1[i1]); i1+=1
                    elif i2<len(s2): merged.append(s2[i2]); i2+=1
                tests.append({"s1":s1,"s2":s2,"s3":"".join(merged)})
            else:
                tests.append({"s1":s1,"s2":s2,"s3":"".join(rng.choices(string.ascii_lowercase[:4],k=len(s1)+len(s2)))})
        return tests
