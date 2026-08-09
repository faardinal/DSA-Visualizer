"""Batch 9 — final NeetCode 250 problems to reach 250 total (LC 10,65,68,149,166,171,172,188,204,256,355,357,396,397,400,517,528,556,632)."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, FloatValidator, Validator, ValidationResult
)
from backend.execution_engine.object_builder import LIST_NODE_HELPERS, TREE_NODE_HELPERS


# LC 10 — Regular Expression Matching
class RegexMatchingPlugin(ProblemPlugin):
    problem_id="regular-expression-matching"; leetcode_number=10
    title="Regular Expression Matching"; slug="regular-expression-matching"
    method_name="isMatch"; difficulty="Hard"; pattern="2-D DP"
    topics=["String","Dynamic Programming","Recursion"]; parameters=["s: str","p: str"]
    return_type="bool"; hidden_test_count=4
    description="Implement regular expression matching with '.' and '*'."
    def get_test_cases(self):
        return [TestCase({"s":"aa","p":"a"},False,"Example 1"),TestCase({"s":"aa","p":"a*"},True,"Example 2"),
                TestCase({"s":"ab","p":".*"},True,"Example 3"),TestCase({"s":"aab","p":"c*a*b"},True,"Example 4")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s,p=inputs["s"],inputs["p"]; m,n=len(s),len(p)
        dp=[[False]*(n+1) for _ in range(m+1)]; dp[0][0]=True
        for j in range(1,n+1):
            if p[j-1]=='*' and j>=2: dp[0][j]=dp[0][j-2]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if p[j-1]=='*':
                    dp[i][j]=dp[i][j-2]
                    if p[j-2]=='.' or p[j-2]==s[i-1]: dp[i][j]|=dp[i-1][j]
                elif p[j-1]=='.' or p[j-1]==s[i-1]: dp[i][j]=dp[i-1][j-1]
        return dp[m][n]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for i in range(count):
            s="".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(1,5)))
            if i%2==0: tests.append({"s":s,"p":s})
            else: tests.append({"s":s,"p":".*"})
        return tests


# LC 171 — Excel Sheet Column Number
class ExcelColumnNumberPlugin(ProblemPlugin):
    problem_id="excel-sheet-column-number"; leetcode_number=171
    title="Excel Sheet Column Number"; slug="excel-sheet-column-number"
    method_name="titleToNumber"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Math","String"]; parameters=["columnTitle: str"]; return_type="int"; hidden_test_count=4
    description="Convert column title string to number (A=1, B=2, ..., Z=26, AA=27)."
    def get_test_cases(self):
        return [TestCase({"columnTitle":"A"},1,"Example 1"),TestCase({"columnTitle":"AB"},28,"Example 2"),
                TestCase({"columnTitle":"ZY"},701,"Example 3"),TestCase({"columnTitle":"Z"},26,"Z",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        result=0
        for c in inputs["columnTitle"]: result=result*26+(ord(c)-64)
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        def num_to_title(n):
            r=""
            while n: n,rem=divmod(n-1,26); r=chr(rem+65)+r
            return r
        return [{"columnTitle":num_to_title(rng.randint(1,702))} for _ in range(count)]


# LC 172 — Factorial Trailing Zeroes
class FactorialTrailingZeroesPlugin(ProblemPlugin):
    problem_id="factorial-trailing-zeroes"; leetcode_number=172
    title="Factorial Trailing Zeroes"; slug="factorial-trailing-zeroes"
    method_name="trailingZeroes"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Return the number of trailing zeroes in n!."
    def get_test_cases(self):
        return [TestCase({"n":3},0,"Example 1"),TestCase({"n":5},1,"Example 2"),TestCase({"n":0},0,"Example 3"),
                TestCase({"n":25},6,"n=25",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; count=0
        while n>=5: n//=5; count+=n
        return count
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,100)} for _ in range(count)]


# LC 204 — Count Primes
class CountPrimesPlugin(ProblemPlugin):
    problem_id="count-primes"; leetcode_number=204; title="Count Primes"
    slug="count-primes"; method_name="countPrimes"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Array","Math","Enumeration","Number Theory"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Return the number of prime numbers less than n."
    def get_test_cases(self):
        return [TestCase({"n":10},4,"Example 1"),TestCase({"n":0},0,"Example 2"),TestCase({"n":1},0,"Example 3"),
                TestCase({"n":20},8,"n=20",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]
        if n<2: return 0
        sieve=[True]*n; sieve[0]=sieve[1]=False
        for i in range(2,int(n**0.5)+1):
            if sieve[i]:
                for j in range(i*i,n,i): sieve[j]=False
        return sum(sieve)
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,200)} for _ in range(count)]


# LC 188 — Best Time to Buy and Sell Stock IV
class StockIVPlugin(ProblemPlugin):
    problem_id="best-time-to-buy-and-sell-stock-iv"; leetcode_number=188
    title="Best Time to Buy and Sell Stock IV"; slug="best-time-to-buy-and-sell-stock-iv"
    method_name="maxProfit"; difficulty="Hard"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["k: int","prices: List[int]"]
    return_type="int"; hidden_test_count=4; description="Find the maximum profit with at most k transactions."
    def get_test_cases(self):
        return [TestCase({"k":2,"prices":[2,4,1]},2,"Example 1"),TestCase({"k":2,"prices":[3,2,6,5,0,3]},7,"Example 2"),
                TestCase({"k":1,"prices":[1,2]},1,"k=1",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        k,prices=inputs["k"],inputs["prices"]; n=len(prices)
        if not prices or k==0: return 0
        if k>=n//2:
            return sum(max(prices[i+1]-prices[i],0) for i in range(n-1))
        buy=[-float('inf')]*k; sell=[0]*k
        for p in prices:
            for i in range(k-1,-1,-1):
                sell[i]=max(sell[i],buy[i]+p)
                buy[i]=max(buy[i],(sell[i-1] if i>0 else 0)-p)
        return sell[k-1]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"k":rng.randint(1,4),"prices":[rng.randint(1,50) for _ in range(rng.randint(2,12))]} for _ in range(count)]


# LC 355 — Design Twitter
_TWITTER_TPL = """{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = Twitter()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "postTweet":
            obj.postTweet(arg[0], arg[1]); out.append(None)
        elif op == "getNewsFeed":
            out.append(obj.getNewsFeed(arg[0]))
        elif op == "follow":
            obj.follow(arg[0], arg[1]); out.append(None)
        elif op == "unfollow":
            obj.unfollow(arg[0], arg[1]); out.append(None)
    print("__RESULT__:")
    print(repr(out))

main()
"""
class DesignTwitterPlugin(ProblemPlugin):
    problem_id="design-twitter"; leetcode_number=355; title="Design Twitter"
    slug="design-twitter"; method_name="postTweet"; difficulty="Medium"; pattern="Heap / Priority Queue"
    topics=["Hash Table","Linked List","Design","Heap"]; parameters=["userId: int","tweetId: int"]
    return_type="None"; hidden_test_count=3; stateful=True
    description="Design a simplified Twitter: post, follow, unfollow, and getNewsFeed."
    def get_test_cases(self):
        return [TestCase(
            {"ops":["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"],
             "args":[[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]},
            [None,None,[5],None,None,[6,5],None,[5]],"Example 1")]
    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_TWITTER_TPL)
    @staticmethod
    def oracle(inputs):
        from collections import defaultdict
        ops,args=inputs["ops"],inputs["args"]
        tweets=[]; follows=defaultdict(set); out=[None]
        time=0
        for op,arg in zip(ops[1:],args[1:]):
            if op=="postTweet":
                tweets.append((time,arg[0],arg[1])); time+=1; out.append(None)
            elif op=="getNewsFeed":
                uid=arg[0]; friends=follows[uid]|{uid}
                feed=sorted([(t,tid) for t,fid,tid in tweets if fid in friends],reverse=True)
                out.append([tid for _,tid in feed[:10]])
            elif op=="follow":
                follows[arg[0]].add(arg[1]); out.append(None)
            elif op=="unfollow":
                follows[arg[0]].discard(arg[1]); out.append(None)
        return out
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            ops=["Twitter"]; args=[[]]
            for _ in range(rng.randint(3,8)):
                op=rng.choice(["postTweet","follow","getNewsFeed"])
                u=rng.randint(1,3)
                if op=="postTweet": ops.append(op); args.append([u,rng.randint(1,100)])
                elif op=="follow":
                    v=rng.randint(1,3)
                    ops.append(op); args.append([u,v])
                else: ops.append(op); args.append([u])
            tests.append({"ops":ops,"args":args})
        return tests


# LC 166 — Fraction to Recurring Decimal
class FractionToRecurringDecimalPlugin(ProblemPlugin):
    problem_id="fraction-to-recurring-decimal"; leetcode_number=166
    title="Fraction to Recurring Decimal"; slug="fraction-to-recurring-decimal"
    method_name="fractionToDecimal"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Hash Table","Math","String"]; parameters=["numerator: int","denominator: int"]
    return_type="str"; hidden_test_count=4; description="Return fraction as string with recurring part in parentheses."
    def get_test_cases(self):
        return [TestCase({"numerator":1,"denominator":2},"0.5","Example 1"),
                TestCase({"numerator":2,"denominator":1},"2","Example 2"),
                TestCase({"numerator":4,"denominator":333},"0.(012)","Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n,d=inputs["numerator"],inputs["denominator"]
        if n%d==0: return str(n//d)
        sign="-" if (n<0)^(d<0) else ""; n,d=abs(n),abs(d)
        integer=n//d; remainder=n%d
        decimal=[]; seen={}
        while remainder:
            if remainder in seen:
                pos=seen[remainder]; decimal.insert(pos,'('); decimal.append(')'); break
            seen[remainder]=len(decimal); remainder*=10; decimal.append(str(remainder//d)); remainder%=d
        return sign+str(integer)+"."+("".join(decimal))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"numerator":rng.randint(-100,100),"denominator":rng.choice([1,2,3,4,5,6,7,8,9,10])} for _ in range(count)]


# LC 357 — Count Numbers with Unique Digits
class CountUniqueDigitsPlugin(ProblemPlugin):
    problem_id="count-numbers-with-unique-digits"; leetcode_number=357
    title="Count Numbers with Unique Digits"; slug="count-numbers-with-unique-digits"
    method_name="countNumbersWithUniqueDigits"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math","Dynamic Programming","Backtracking"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Count all numbers with unique digits in range [0, 10^n)."
    def get_test_cases(self):
        return [TestCase({"n":2},91,"Example 1"),TestCase({"n":0},1,"Example 2"),
                TestCase({"n":1},10,"n=1",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]
        if n==0: return 1
        result=10; unique=9; avail=9
        for i in range(2,min(n+1,11)):
            unique*=avail; result+=unique; avail-=1
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,8)} for _ in range(count)]


# LC 397 — Integer Replacement
class IntegerReplacementPlugin(ProblemPlugin):
    problem_id="integer-replacement"; leetcode_number=397
    title="Integer Replacement"; slug="integer-replacement"
    method_name="integerReplacement"; difficulty="Medium"; pattern="Bit Manipulation"
    topics=["Dynamic Programming","Greedy","Bit Manipulation","Memoization"]
    parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Return minimum number of replacements to reduce n to 1."
    def get_test_cases(self):
        return [TestCase({"n":8},3,"Example 1"),TestCase({"n":7},4,"Example 2"),TestCase({"n":4},2,"n=4",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; steps=0
        while n!=1:
            if n%2==0: n//=2
            elif n==3 or bin(n).count('1',2)<=1: n-=1
            else: n+=1
            steps+=1
        return steps
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(1,1000)} for _ in range(count)]


# LC 400 — Nth Digit
class NthDigitPlugin(ProblemPlugin):
    problem_id="nth-digit"; leetcode_number=400; title="Nth Digit"
    slug="nth-digit"; method_name="findNthDigit"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math","Binary Search"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Find the nth digit of the infinite sequence 123456789101112..."
    def get_test_cases(self):
        return [TestCase({"n":3},3,"Example 1"),TestCase({"n":11},0,"Example 2"),
                TestCase({"n":1},1,"n=1",is_hidden=True),TestCase({"n":15},2,"n=15",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; digits=1; count=9; start=1
        while n>digits*count: n-=digits*count; digits+=1; count*=10; start*=10
        num=start+(n-1)//digits; return int(str(num)[(n-1)%digits])
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(1,200)} for _ in range(count)]


# LC 149 — Max Points on a Line
class MaxPointsOnLinePlugin(ProblemPlugin):
    problem_id="max-points-on-a-line"; leetcode_number=149; title="Max Points on a Line"
    slug="max-points-on-a-line"; method_name="maxPoints"; difficulty="Hard"; pattern="Math & Geometry"
    topics=["Array","Hash Table","Math","Geometry"]; parameters=["points: List[List[int]]"]
    return_type="int"; hidden_test_count=4; description="Find maximum number of points that lie on the same straight line."
    def get_test_cases(self):
        return [TestCase({"points":[[1,1],[2,2],[3,3]]},3,"Example 1"),
                TestCase({"points":[[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]},4,"Example 2"),
                TestCase({"points":[[1,1]]},1,"Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        from collections import defaultdict; from math import gcd
        pts=inputs["points"]; n=len(pts)
        if n<=2: return n
        best=2
        for i in range(n):
            slopes=defaultdict(int)
            for j in range(i+1,n):
                dy=pts[j][1]-pts[i][1]; dx=pts[j][0]-pts[i][0]
                if dx==0: key=(float('inf'),0)
                else:
                    g=gcd(abs(dy),abs(dx)); sign=-1 if (dy<0)^(dx<0) else 1
                    key=(sign*abs(dy)//g,abs(dx)//g)
                slopes[key]+=1
            best=max(best,max(slopes.values())+1) if slopes else best
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            base_x=rng.randint(0,5); base_y=rng.randint(0,5); dx=rng.randint(1,3); dy=rng.randint(1,3)
            pts=[[base_x+i*dx,base_y+i*dy] for i in range(rng.randint(3,5))]
            pts+=[[rng.randint(0,10),rng.randint(0,10)] for _ in range(rng.randint(0,3))]
            tests.append({"points":pts})
        return tests


# LC 256 — Paint House
class PaintHousePlugin(ProblemPlugin):
    problem_id="paint-house"; leetcode_number=256; title="Paint House"
    slug="paint-house"; method_name="minCost"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","Dynamic Programming"]; parameters=["costs: List[List[int]]"]
    return_type="int"; hidden_test_count=4; description="Minimum cost to paint all houses with 3 colors where adjacent houses can't have same color."
    def get_test_cases(self):
        return [TestCase({"costs":[[17,2,17],[16,16,5],[14,3,19]]},10,"Example 1"),
                TestCase({"costs":[[7,6,2]]},2,"Single house")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        costs=inputs["costs"]
        if not costs: return 0
        dp=costs[0][:]
        for i in range(1,len(costs)):
            dp=[costs[i][0]+min(dp[1],dp[2]),costs[i][1]+min(dp[0],dp[2]),costs[i][2]+min(dp[0],dp[1])]
        return min(dp)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"costs":[[rng.randint(1,20) for _ in range(3)] for _ in range(rng.randint(1,8))]} for _ in range(count)]


# LC 396 — Rotate Function
class RotateFunctionPlugin(ProblemPlugin):
    problem_id="rotate-function"; leetcode_number=396; title="Rotate Function"
    slug="rotate-function"; method_name="maxRotateFunction"; difficulty="Medium"; pattern="Array"
    topics=["Array","Math","Dynamic Programming"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4
    description="Find the max value of F(k) = sum(i * nums[(i+k) % n]) over all rotations k."
    def get_test_cases(self):
        return [TestCase({"nums":[4,3,2,6]},26,"Example 1"),TestCase({"nums":[1]},0,"Single")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; n=len(nums); s=sum(nums)
        f=sum(i*v for i,v in enumerate(nums)); best=f
        for k in range(1,n):
            f+=s-n*nums[n-k]; best=max(best,f)
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,10) for _ in range(rng.randint(2,8))]} for _ in range(count)]


# LC 517 — Super Washing Machines
class SuperWashingMachinesPlugin(ProblemPlugin):
    problem_id="super-washing-machines"; leetcode_number=517; title="Super Washing Machines"
    slug="super-washing-machines"; method_name="findMinMoves"; difficulty="Hard"; pattern="Greedy"
    topics=["Array","Greedy"]; parameters=["machines: List[int]"]; return_type="int"; hidden_test_count=4
    description="Find minimum moves to equalize the load. Return -1 if impossible."
    def get_test_cases(self):
        return [TestCase({"machines":[1,0,5]},3,"Example 1"),TestCase({"machines":[0,3,0]},2,"Example 2"),
                TestCase({"machines":[0,2,0]},-1,"Example 3: impossible")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        m=inputs["machines"]; n=len(m); s=sum(m)
        if s%n: return -1
        target=s//n; best=prefix=0
        for v in m:
            prefix+=v-target; best=max(best,abs(prefix),v-target)
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,6); total=rng.randint(1,5)*n
            m=[0]*n
            for _ in range(total): m[rng.randint(0,n-1)]+=1
            tests.append({"machines":m})
        return tests


# LC 528 — Random Pick with Weight
_RANDOM_PICK_TPL = """{imports}
{helpers}
{solution_code}

def main():
    import random
    random.seed(42)
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = Solution(args[0][0])
    for op, arg in zip(ops[1:], args[1:]):
        if op == "pickIndex":
            out.append(obj.pickIndex())
    print("__RESULT__:")
    print(repr(out))

main()
"""
class RandomPickWeightPlugin(ProblemPlugin):
    problem_id="random-pick-with-weight"; leetcode_number=528
    title="Random Pick with Weight"; slug="random-pick-with-weight"
    method_name="pickIndex"; difficulty="Medium"; pattern="Array"
    topics=["Array","Math","Binary Search","Prefix Sum","Randomized"]
    parameters=["w: List[int]"]; return_type="int"; hidden_test_count=3; stateful=True
    description="Randomly pick an index with probability proportional to w[i]."
    def get_test_cases(self):
        return [TestCase({"ops":["Solution","pickIndex"],"args":[[[1]],[]]},
                         [None,0],"Example 1")]
    def get_validator(self): return RandomPickValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_RANDOM_PICK_TPL)
    @staticmethod
    def oracle(inputs):
        ops,args=inputs["ops"],inputs["args"]; weights=args[0][0]
        n=len(weights); out=[None]
        for op in ops[1:]:
            if op=="pickIndex": out.append(0)  # oracle just validates index range
        return out
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            w=[rng.randint(1,10) for _ in range(rng.randint(2,5))]
            tests.append({"ops":["Solution","pickIndex","pickIndex"],"args":[[w],[],[]]})
        return tests

class RandomPickValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # Just check all results are valid indices
        w=inputs.get("args",[[]])[0][0] if inputs else []
        n=len(w)
        for v in actual:
            if v is None: continue
            if not (0<=v<n): return ValidationResult(False,f"index in [0,{n-1}]",repr(v),f"Invalid index {v}")
        return ValidationResult(True,repr(expected),repr(actual),"")


# LC 556 — Next Greater Element III
class NextGreaterElementIIIPlugin(ProblemPlugin):
    problem_id="next-greater-element-iii"; leetcode_number=556
    title="Next Greater Element III"; slug="next-greater-element-iii"
    method_name="nextGreaterElement"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math","Two Pointers","String"]; parameters=["n: int"]; return_type="int"; hidden_test_count=4
    description="Find smallest integer greater than n using same digits. Return -1 if none."
    def get_test_cases(self):
        return [TestCase({"n":12},21,"Example 1"),TestCase({"n":21},-1,"Example 2"),
                TestCase({"n":123},132,"Three digits",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; digits=list(str(n)); sz=len(digits); i=sz-2
        while i>=0 and digits[i]>=digits[i+1]: i-=1
        if i<0: return -1
        j=sz-1
        while digits[j]<=digits[i]: j-=1
        digits[i],digits[j]=digits[j],digits[i]; digits[i+1:]=digits[i+1:][::-1]
        result=int("".join(digits))
        return result if result<2**31 else -1
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"n":rng.randint(12,99999)} for _ in range(count)]


# LC 632 — Smallest Range Covering Elements from K Lists
class SmallestRangePlugin(ProblemPlugin):
    problem_id="smallest-range-covering-elements-from-k-lists"; leetcode_number=632
    title="Smallest Range Covering Elements from K Lists"
    slug="smallest-range-covering-elements-from-k-lists"
    method_name="smallestRange"; difficulty="Hard"; pattern="Heap / Priority Queue"
    topics=["Array","Hash Table","Greedy","Sliding Window","Sorting","Heap"]
    parameters=["nums: List[List[int]]"]; return_type="List[int]"; hidden_test_count=3
    description="Find the smallest range that includes at least one number from each of k lists."
    def get_test_cases(self):
        return [TestCase({"nums":[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]},[-1,24],"Example 1: check range"),
                TestCase({"nums":[[1,2,3],[1,2,3],[1,2,3]]},[1,1],"All same")]
    def get_validator(self): return SmallestRangeValidator()
    @staticmethod
    def oracle(inputs):
        import heapq
        nums=inputs["nums"]; heap=[(nums[i][0],i,0) for i in range(len(nums))]
        heapq.heapify(heap); cur_max=max(row[0] for row in nums)
        best_range=float('inf'); best=[0,cur_max]
        while heap:
            cur_min,i,j=heapq.heappop(heap)
            if cur_max-cur_min<best_range: best_range=cur_max-cur_min; best=[cur_min,cur_max]
            if j+1==len(nums[i]): break
            next_val=nums[i][j+1]; cur_max=max(cur_max,next_val); heapq.heappush(heap,(next_val,i,j+1))
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            k=rng.randint(2,4)
            tests.append({"nums":[sorted(rng.randint(1,30) for _ in range(rng.randint(2,5))) for _ in range(k)]})
        return tests

class SmallestRangeValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # Check it's a valid range containing at least one from each list
        lo,hi=actual
        if inputs:
            for lst in inputs.get("nums",[]):
                if not any(lo<=v<=hi for v in lst):
                    return ValidationResult(False,repr(expected),repr(actual),f"List {lst} not covered")
        # Check same width as expected
        passed=(hi-lo)==(expected[1]-expected[0])
        return ValidationResult(passed,repr(expected),repr(actual),"" if passed else "Different range size")
