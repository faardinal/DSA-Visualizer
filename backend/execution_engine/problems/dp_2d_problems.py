"""2-D Dynamic Programming pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator


# LC 62 — Unique Paths
class UniquePathsPlugin(ProblemPlugin):
    problem_id="unique-paths"; leetcode_number=62; title="Unique Paths"; slug="unique-paths"
    method_name="uniquePaths"; difficulty="Medium"; pattern="2-D DP"
    topics=["Math","Dynamic Programming","Combinatorics"]; parameters=["m: int","n: int"]
    return_type="int"; hidden_test_count=4; description="Count unique paths in m×n grid from top-left to bottom-right."

    def get_test_cases(self):
        return [TestCase({"m":3,"n":7},28,"Example 1"),TestCase({"m":3,"n":2},3,"Example 2"),
                TestCase({"m":1,"n":1},1,"1x1",is_hidden=True),TestCase({"m":5,"n":5},70,"5x5",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        m,n=inputs["m"],inputs["n"]
        dp=[[1]*n for _ in range(m)]
        for i in range(1,m):
            for j in range(1,n): dp[i][j]=dp[i-1][j]+dp[i][j-1]
        return dp[m-1][n-1]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"m":rng.randint(1,10),"n":rng.randint(1,10)} for _ in range(count)]


# LC 64 — Minimum Path Sum
class MinimumPathSumPlugin(ProblemPlugin):
    problem_id="minimum-path-sum"; leetcode_number=64; title="Minimum Path Sum"; slug="minimum-path-sum"
    method_name="minPathSum"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","Dynamic Programming","Matrix"]; parameters=["grid: List[List[int]]"]
    return_type="int"; hidden_test_count=4; description="Find minimum sum path from top-left to bottom-right."

    def get_test_cases(self):
        return [TestCase({"grid":[[1,3,1],[1,5,1],[4,2,1]]},7,"Example 1"),
                TestCase({"grid":[[1,2,3],[4,5,6]]},12,"Example 2"),
                TestCase({"grid":[[1]]},1,"1x1",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        grid=[row[:] for row in inputs["grid"]]
        m,n=len(grid),len(grid[0])
        for i in range(m):
            for j in range(n):
                if i==0 and j==0: continue
                elif i==0: grid[i][j]+=grid[i][j-1]
                elif j==0: grid[i][j]+=grid[i-1][j]
                else: grid[i][j]+=min(grid[i-1][j],grid[i][j-1])
        return grid[m-1][n-1]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            r=rng.randint(1,5); c=rng.randint(1,5)
            tests.append({"grid":[[rng.randint(1,9) for _ in range(c)] for _ in range(r)]})
        return tests


# LC 309 — Best Time to Buy and Sell Stock with Cooldown
class StockCooldownPlugin(ProblemPlugin):
    problem_id="best-time-to-buy-and-sell-stock-with-cooldown"; leetcode_number=309
    title="Best Time to Buy and Sell Stock with Cooldown"; slug="best-time-to-buy-and-sell-stock-with-cooldown"
    method_name="maxProfit"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["prices: List[int]"]
    return_type="int"; hidden_test_count=4; description="Max profit with cooldown after sell."

    def get_test_cases(self):
        return [TestCase({"prices":[1,2,3,0,2]},3,"Example 1"),TestCase({"prices":[1]},0,"Single"),
                TestCase({"prices":[1,2]},1,"Two days",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        prices=inputs["prices"]
        if len(prices)<2: return 0
        hold,sold,rest=float('-inf'),0,0
        for p in prices:
            hold,sold,rest=max(hold,rest-p),hold+p,max(rest,sold)
        return max(sold,rest)

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"prices":[rng.randint(1,50) for _ in range(rng.randint(2,15))]} for _ in range(count)]


# LC 518 — Coin Change II
class CoinChangeIIPlugin(ProblemPlugin):
    problem_id="coin-change-ii"; leetcode_number=518; title="Coin Change II"; slug="coin-change-ii"
    method_name="change"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["amount: int","coins: List[int]"]
    return_type="int"; hidden_test_count=4; description="Return the number of combinations to make up the amount."

    def get_test_cases(self):
        return [TestCase({"amount":5,"coins":[1,2,5]},4,"Example 1"),
                TestCase({"amount":3,"coins":[2]},0,"Example 2"),
                TestCase({"amount":10,"coins":[10]},1,"Example 3"),
                TestCase({"amount":0,"coins":[1,2]},1,"Amount 0",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        amount,coins=inputs["amount"],inputs["coins"]
        dp=[0]*(amount+1); dp[0]=1
        for coin in coins:
            for i in range(coin,amount+1): dp[i]+=dp[i-coin]
        return dp[amount]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            coins=list(set(rng.randint(1,10) for _ in range(rng.randint(1,5))))
            amount=rng.randint(0,20)
            tests.append({"amount":amount,"coins":coins})
        return tests


# LC 494 — Target Sum
class TargetSumPlugin(ProblemPlugin):
    problem_id="target-sum"; leetcode_number=494; title="Target Sum"; slug="target-sum"
    method_name="findTargetSumWays"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","Dynamic Programming","Backtracking"]; parameters=["nums: List[int]","target: int"]
    return_type="int"; hidden_test_count=4; description="Count number of ways to assign +/- to reach target."

    def get_test_cases(self):
        return [TestCase({"nums":[1,1,1,1,1],"target":3},5,"Example 1"),
                TestCase({"nums":[1],"target":1},1,"Example 2"),
                TestCase({"nums":[1],"target":-1},1,"Negative target",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums,target=inputs["nums"],inputs["target"]
        dp={0:1}
        for n in nums:
            ndp={}
            for s,cnt in dp.items():
                ndp[s+n]=ndp.get(s+n,0)+cnt
                ndp[s-n]=ndp.get(s-n,0)+cnt
            dp=ndp
        return dp.get(target,0)

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            nums=[rng.randint(1,5) for _ in range(rng.randint(2,8))]
            target=rng.randint(-sum(nums),sum(nums))
            tests.append({"nums":nums,"target":target})
        return tests


# LC 72 — Edit Distance
class EditDistancePlugin(ProblemPlugin):
    problem_id="edit-distance"; leetcode_number=72; title="Edit Distance"; slug="edit-distance"
    method_name="minDistance"; difficulty="Medium"; pattern="2-D DP"
    topics=["String","Dynamic Programming"]; parameters=["word1: str","word2: str"]
    return_type="int"; hidden_test_count=4; description="Minimum operations to convert word1 to word2."

    def get_test_cases(self):
        return [TestCase({"word1":"horse","word2":"ros"},3,"Example 1"),
                TestCase({"word1":"intention","word2":"execution"},5,"Example 2"),
                TestCase({"word1":"","word2":"a"},1,"Empty to single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        w1,w2=inputs["word1"],inputs["word2"]
        m,n=len(w1),len(w2)
        dp=list(range(n+1))
        for i in range(1,m+1):
            prev=dp[0]; dp[0]=i
            for j in range(1,n+1):
                tmp=dp[j]
                if w1[i-1]==w2[j-1]: dp[j]=prev
                else: dp[j]=1+min(prev,dp[j],dp[j-1])
                prev=tmp
        return dp[n]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        return [{"word1":"".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(0,6))),
                 "word2":"".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(0,6)))} for _ in range(count)]


# LC 312 — Burst Balloons
class BurstBalloonsPlugin(ProblemPlugin):
    problem_id="burst-balloons"; leetcode_number=312; title="Burst Balloons"; slug="burst-balloons"
    method_name="maxCoins"; difficulty="Hard"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=3; description="Collect maximum coins by bursting all balloons."

    def get_test_cases(self):
        return [TestCase({"nums":[3,1,5,8]},167,"Example 1"),TestCase({"nums":[1,5]},10,"Example 2"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=[1]+inputs["nums"]+[1]; n=len(nums)
        dp=[[0]*n for _ in range(n)]
        for length in range(2,n):
            for left in range(0,n-length):
                right=left+length
                for k in range(left+1,right):
                    dp[left][right]=max(dp[left][right],
                        nums[left]*nums[k]*nums[right]+dp[left][k]+dp[k][right])
        return dp[0][n-1]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,10) for _ in range(rng.randint(1,8))]} for _ in range(count)]
