"""Batch 10 — final 14 problems to reach 250."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, AnyOrderListValidator, Validator, ValidationResult
)
from backend.execution_engine.object_builder import LIST_NODE_HELPERS, TREE_NODE_HELPERS


# LC 65 — Valid Number
class ValidNumberPlugin(ProblemPlugin):
    problem_id="valid-number"; leetcode_number=65; title="Valid Number"
    slug="valid-number"; method_name="isNumber"; difficulty="Hard"; pattern="Array"
    topics=["String"]; parameters=["s: str"]; return_type="bool"; hidden_test_count=4
    description="Determine if the given string is a valid number."
    def get_test_cases(self):
        return [TestCase({"s":"0"},True,"Example 1"),TestCase({"s":"e"},False,"Example 2"),
                TestCase({"s":"."},False,"Example 3"),TestCase({"s":"2e0"},True,"Sci notation"),
                TestCase({"s":"-.5"},True,"Negative decimal",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        s=inputs["s"].strip()
        if not s: return False
        i=0; has_digit=False; has_dot=False; has_e=False
        if i<len(s) and s[i] in '+-': i+=1
        while i<len(s):
            c=s[i]
            if c.isdigit(): has_digit=True
            elif c=='.':
                if has_dot or has_e: return False
                has_dot=True
            elif c in 'eE':
                if has_e or not has_digit: return False
                has_e=True; has_digit=False
                if i+1<len(s) and s[i+1] in '+-': i+=1
            else: return False
            i+=1
        return has_digit
    @staticmethod
    def generate_hidden_inputs(rng,count):
        samples=["0","0.1",".5","2e10","-2.5e3","abc","--1","2e","e3","1.2.3","  ","1 2","+.8","46.e3"]
        return [{"s":rng.choice(samples)} for _ in range(count)]


# LC 68 — Text Justification
class TextJustificationPlugin(ProblemPlugin):
    problem_id="text-justification"; leetcode_number=68; title="Text Justification"
    slug="text-justification"; method_name="fullJustify"; difficulty="Hard"; pattern="Array"
    topics=["Array","String","Simulation"]; parameters=["words: List[str]","maxWidth: int"]
    return_type="List[str]"; hidden_test_count=3; description="Justify words to maxWidth by distributing spaces."
    def get_test_cases(self):
        return [TestCase({"words":["This","is","an","example","of","text","justification."],"maxWidth":16},
                         ["This    is    an","example  of text","justification.  "],"Example 1"),
                TestCase({"words":["What","must","be","acknowledgment","shall","be"],"maxWidth":16},
                         ["What   must   be","acknowledgment  ","shall be        "],"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        words,maxWidth=inputs["words"],inputs["maxWidth"]
        lines=[]; i=0
        while i<len(words):
            line=[words[i]]; cur_len=len(words[i]); i+=1
            while i<len(words) and cur_len+1+len(words[i])<=maxWidth:
                cur_len+=1+len(words[i]); line.append(words[i]); i+=1
            if i==len(words) or len(line)==1:
                row=" ".join(line); lines.append(row+(maxWidth-len(row))*" ")
            else:
                total_spaces=maxWidth-sum(len(w) for w in line); gaps=len(line)-1
                q,r=divmod(total_spaces,gaps)
                row=""
                for j,w in enumerate(line):
                    row+=w
                    if j<gaps: row+=" "*(q+(1 if j<r else 0))
                lines.append(row)
        return lines
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        tests=[]
        for _ in range(count):
            words=["".join(rng.choices(string.ascii_lowercase,k=rng.randint(2,6))) for _ in range(rng.randint(3,8))]
            tests.append({"words":words,"maxWidth":16})
        return tests


# LC 90 — Subsets II
class SubsetsIIPlugin(ProblemPlugin):
    problem_id="subsets-ii"; leetcode_number=90; title="Subsets II"
    slug="subsets-ii"; method_name="subsetsWithDup"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking","Bit Manipulation"]; parameters=["nums: List[int]"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Return all possible subsets of nums which may contain duplicates."
    def get_test_cases(self):
        return [TestCase({"nums":[1,2,2]},[[],[1],[1,2],[1,2,2],[2],[2,2]],"Example 1"),
                TestCase({"nums":[0]},[[],[0]],"Example 2")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import AnyOrderListValidator; return AnyOrderListValidator()
    @staticmethod
    def oracle(inputs):
        nums=sorted(inputs["nums"]); result=set(); result.add(())
        for n in nums: result|={s+(n,) for s in result}
        return [list(s) for s in result]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,4) for _ in range(rng.randint(2,5))]} for _ in range(count)]


# LC 79 — Word Search
class WordSearchPlugin(ProblemPlugin):
    problem_id="word-search"; leetcode_number=79; title="Word Search"
    slug="word-search"; method_name="exist"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking","Matrix"]; parameters=["board: List[List[str]]","word: str"]
    return_type="bool"; hidden_test_count=4; description="Return true if word exists sequentially in the grid."
    def get_test_cases(self):
        return [TestCase({"board":[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"word":"ABCCED"},True,"Example 1"),
                TestCase({"board":[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"word":"SEE"},True,"Example 2"),
                TestCase({"board":[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"word":"ABCB"},False,"Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        board,word=inputs["board"],inputs["word"]
        rows,cols=len(board),len(board[0]) if board else 0
        def dfs(r,c,i,visited):
            if i==len(word): return True
            if r<0 or r>=rows or c<0 or c>=cols or (r,c) in visited or board[r][c]!=word[i]: return False
            visited.add((r,c))
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                if dfs(r+dr,c+dc,i+1,visited): visited.remove((r,c)); return True
            visited.remove((r,c)); return False
        for r in range(rows):
            for c in range(cols):
                if dfs(r,c,0,set()): return True
        return False
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for i in range(count):
            board=[[rng.choice("ABCDEF") for _ in range(4)] for _ in range(4)]
            if i%2==0:
                flat=[c for row in board for c in row]
                word="".join(rng.choices(flat,k=rng.randint(2,4)))
            else: word="".join(rng.choices("ABCDEF",k=3))
            tests.append({"board":board,"word":word})
        return tests


# LC 332 already done. LC 474 — Ones and Zeroes
class OnesAndZeroesPlugin(ProblemPlugin):
    problem_id="ones-and-zeroes"; leetcode_number=474; title="Ones and Zeroes"
    slug="ones-and-zeroes"; method_name="findMaxForm"; difficulty="Medium"; pattern="2-D DP"
    topics=["Array","String","Dynamic Programming"]; parameters=["strs: List[str]","m: int","n: int"]
    return_type="int"; hidden_test_count=4; description="Find max subset size where total 0s <= m and total 1s <= n."
    def get_test_cases(self):
        return [TestCase({"strs":["10","0001","111001","1","0"],"m":5,"n":3},4,"Example 1"),
                TestCase({"strs":["10","0","1"],"m":1,"n":1},2,"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        strs,m,n=inputs["strs"],inputs["m"],inputs["n"]
        dp=[[0]*(n+1) for _ in range(m+1)]
        for s in strs:
            zeros=s.count('0'); ones=s.count('1')
            for i in range(m,zeros-1,-1):
                for j in range(n,ones-1,-1):
                    dp[i][j]=max(dp[i][j],dp[i-zeros][j-ones]+1)
        return dp[m][n]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"strs":["".join(rng.choices("01",k=rng.randint(1,6))) for _ in range(rng.randint(3,8))],"m":rng.randint(2,6),"n":rng.randint(2,6)} for _ in range(count)]


# LC 238 already done. LC 295 already done. LC 310 already done.
# LC 344 already done. LC 347 already done. LC 349 already done.

# LC 485 — Max Consecutive Ones
class MaxConsecutiveOnesPlugin(ProblemPlugin):
    problem_id="max-consecutive-ones"; leetcode_number=485; title="Max Consecutive Ones"
    slug="max-consecutive-ones"; method_name="findMaxConsecutiveOnes"; difficulty="Easy"; pattern="Array"
    topics=["Array"]; parameters=["nums: List[int]"]; return_type="int"; hidden_test_count=4
    description="Return the maximum number of consecutive 1s in a binary array."
    def get_test_cases(self):
        return [TestCase({"nums":[1,1,0,1,1,1]},3,"Example 1"),TestCase({"nums":[1,0,1,1,0,1]},2,"Example 2"),
                TestCase({"nums":[0]},0,"All zeros",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; best=cur=0
        for n in nums:
            if n==1: cur+=1; best=max(best,cur)
            else: cur=0
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(0,1) for _ in range(rng.randint(1,15))]} for _ in range(count)]


# LC 509 — Fibonacci Number
class FibonacciPlugin(ProblemPlugin):
    problem_id="fibonacci-number"; leetcode_number=509; title="Fibonacci Number"
    slug="fibonacci-number"; method_name="fib"; difficulty="Easy"; pattern="1-D DP"
    topics=["Math","Dynamic Programming","Recursion","Memoization"]; parameters=["n: int"]
    return_type="int"; hidden_test_count=4; description="Return the nth Fibonacci number."
    def get_test_cases(self):
        return [TestCase({"n":2},1,"Example 1"),TestCase({"n":3},2,"Example 2"),TestCase({"n":4},3,"Example 3"),
                TestCase({"n":0},0,"n=0",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]
        if n<=1: return n
        a,b=0,1
        for _ in range(2,n+1): a,b=b,a+b
        return b
    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,20)} for _ in range(count)]


# LC 338 already done. LC 371 already done.
# LC 448 — Find All Numbers Disappeared in an Array
class FindDisappearedNumbersPlugin(ProblemPlugin):
    problem_id="find-all-numbers-disappeared-in-an-array"; leetcode_number=448
    title="Find All Numbers Disappeared in an Array"; slug="find-all-numbers-disappeared-in-an-array"
    method_name="findDisappearedNumbers"; difficulty="Easy"; pattern="Array"
    topics=["Array","Hash Table"]; parameters=["nums: List[int]"]; return_type="List[int]"; hidden_test_count=4
    description="Return all integers in [1,n] that do not appear in nums."
    def get_test_cases(self):
        return [TestCase({"nums":[4,3,2,7,8,2,3,1]},[5,6],"Example 1"),TestCase({"nums":[1,1]},[2],"Example 2"),
                TestCase({"nums":[1]},[],"Complete",is_hidden=True)]
    def get_validator(self): return SortedListValidator()
    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; s=set(nums); n=len(nums)
        return sorted(i for i in range(1,n+1) if i not in s)
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,10); nums=[rng.randint(1,n) for _ in range(n)]; tests.append({"nums":nums})
        return tests


# LC 506 — Relative Ranks
class RelativeRanksPlugin(ProblemPlugin):
    problem_id="relative-ranks"; leetcode_number=506; title="Relative Ranks"
    slug="relative-ranks"; method_name="findRelativeRanks"; difficulty="Easy"; pattern="Array"
    topics=["Array","Sorting","Heap"]; parameters=["score: List[int]"]; return_type="List[str]"; hidden_test_count=4
    description="Assign ranks (Gold/Silver/Bronze/rank-number) based on scores."
    def get_test_cases(self):
        return [TestCase({"score":[5,4,3,2,1]},["Gold Medal","Silver Medal","Bronze Medal","4","5"],"Example 1"),
                TestCase({"score":[10,3,8,9,4]},["Gold Medal","5","Bronze Medal","Silver Medal","4"],"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        score=inputs["score"]; n=len(score); rank_map={}
        medals=["Gold Medal","Silver Medal","Bronze Medal"]
        for i,s in enumerate(sorted(score,reverse=True)):
            rank_map[s]=medals[i] if i<3 else str(i+1)
        return [rank_map[s] for s in score]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"score":rng.sample(range(1,1000),rng.randint(2,8))} for _ in range(count)]


# LC 557 — Reverse Words in a String III
class ReverseWordsIIIPlugin(ProblemPlugin):
    problem_id="reverse-words-in-a-string-iii"; leetcode_number=557
    title="Reverse Words in a String III"; slug="reverse-words-in-a-string-iii"
    method_name="reverseWords"; difficulty="Easy"; pattern="Two Pointers"
    topics=["Two Pointers","String"]; parameters=["s: str"]; return_type="str"; hidden_test_count=4
    description="Reverse the characters in each word while preserving whitespace and word order."
    def get_test_cases(self):
        return [TestCase({"s":"Let's take LeetCode contest"},"s'teL ekat edoCteeL tsetnoc","Example 1"),
                TestCase({"s":"Mr Ding"},"rM gniD","Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs): return " ".join(w[::-1] for w in inputs["s"].split())
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; return [{"s":" ".join("".join(rng.choices(string.ascii_lowercase,k=rng.randint(2,6))) for _ in range(rng.randint(1,4)))} for _ in range(count)]


# LC 566 — Reshape the Matrix
class ReshapeMatrixPlugin(ProblemPlugin):
    problem_id="reshape-the-matrix"; leetcode_number=566; title="Reshape the Matrix"
    slug="reshape-the-matrix"; method_name="matrixReshape"; difficulty="Easy"; pattern="Array"
    topics=["Array","Matrix","Simulation"]; parameters=["mat: List[List[int]]","r: int","c: int"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Reshape a matrix to r rows and c columns, or return original if impossible."
    def get_test_cases(self):
        return [TestCase({"mat":[[1,2],[3,4]],"r":1,"c":4},[[1,2,3,4]],"Example 1"),
                TestCase({"mat":[[1,2],[3,4]],"r":2,"c":4},[[1,2],[3,4]],"Example 2: impossible")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        mat,r,c=inputs["mat"],inputs["r"],inputs["c"]
        flat=[v for row in mat for v in row]
        if len(flat)!=r*c: return mat
        return [flat[i*c:(i+1)*c] for i in range(r)]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            rows=rng.randint(2,4); cols=rng.randint(2,4)
            mat=[[rng.randint(1,10) for _ in range(cols)] for _ in range(rows)]
            if i%2==0:
                total=rows*cols; r2=rng.choice([d for d in range(1,total+1) if total%d==0]); c2=total//r2
                tests.append({"mat":mat,"r":r2,"c":c2})
            else: tests.append({"mat":mat,"r":rows+1,"c":cols})
        return tests


# LC 594 — Longest Harmonious Subsequence
class LongestHarmoniousSubsequencePlugin(ProblemPlugin):
    problem_id="longest-harmonious-subsequence"; leetcode_number=594
    title="Longest Harmonious Subsequence"; slug="longest-harmonious-subsequence"
    method_name="findLHS"; difficulty="Easy"; pattern="Hashing"
    topics=["Array","Hash Table","Sorting","Sliding Window"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4
    description="Find the longest subsequence where max-min == 1."
    def get_test_cases(self):
        return [TestCase({"nums":[1,3,2,2,5,2,3,7]},5,"Example 1"),TestCase({"nums":[1,2,3,4]},2,"Example 2"),
                TestCase({"nums":[1,1,1,1]},0,"All same")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; cnt=Counter(inputs["nums"]); best=0
        for k in cnt:
            if k+1 in cnt: best=max(best,cnt[k]+cnt[k+1])
        return best
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,8) for _ in range(rng.randint(3,15))]} for _ in range(count)]


# LC 598 — Range Addition II
class RangeAdditionIIPlugin(ProblemPlugin):
    problem_id="range-addition-ii"; leetcode_number=598; title="Range Addition II"
    slug="range-addition-ii"; method_name="maxCount"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Array","Math"]; parameters=["m: int","n: int","ops: List[List[int]]"]
    return_type="int"; hidden_test_count=4
    description="Count cells with max value after ops (each op increments top-left rectangle)."
    def get_test_cases(self):
        return [TestCase({"m":3,"n":3,"ops":[[2,2],[3,3]]},4,"Example 1"),TestCase({"m":3,"n":3,"ops":[]},9,"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        m,n,ops=inputs["m"],inputs["n"],inputs["ops"]
        if not ops: return m*n
        min_r=min(op[0] for op in ops); min_c=min(op[1] for op in ops)
        return min_r*min_c
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            m,n=rng.randint(2,8),rng.randint(2,8)
            ops=[[rng.randint(1,m),rng.randint(1,n)] for _ in range(rng.randint(0,5))]
            tests.append({"m":m,"n":n,"ops":ops})
        return tests


# LC 643 — Maximum Average Subarray I
class MaxAverageSubarrayIPlugin(ProblemPlugin):
    problem_id="maximum-average-subarray-i"; leetcode_number=643
    title="Maximum Average Subarray I"; slug="maximum-average-subarray-i"
    method_name="findMaxAverage"; difficulty="Easy"; pattern="Sliding Window"
    topics=["Array","Sliding Window"]; parameters=["nums: List[int]","k: int"]
    return_type="float"; hidden_test_count=4; description="Find the contiguous subarray of length k with maximum average."
    def get_test_cases(self):
        return [TestCase({"nums":[1,12,-5,-6,50,3],"k":4},12.75,"Example 1"),
                TestCase({"nums":[5],"k":1},5.0,"Single")]
    def get_validator(self):
        return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums,k=inputs["nums"],inputs["k"]
        window=sum(nums[:k]); best=window
        for i in range(k,len(nums)): window+=nums[i]-nums[i-k]; best=max(best,window)
        return best/k
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(3,15); k=rng.randint(1,n)
            tests.append({"nums":[rng.randint(-10,50) for _ in range(n)],"k":k})
        return tests
