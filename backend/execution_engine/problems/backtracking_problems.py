"""Backtracking pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult


def _sorted_perms(result): return sorted(tuple(sorted(x)) for x in result)
def _sorted_exact(result): return sorted(tuple(x) for x in result)

class UnorderedSubsetValidator(Validator):
    """Validates result is the same set of subsets (any inner/outer order)."""
    def validate(self, actual, expected, inputs=None):
        try:
            a=sorted(tuple(sorted(x)) for x in actual)
            e=sorted(tuple(sorted(x)) for x in expected)
            passed=a==e
        except Exception: passed=False; a,e=actual,expected
        return ValidationResult(passed,repr(e),repr(a),"" if passed else "Subsets differ")

class UnorderedListOfListsValidator(Validator):
    """Validates result is the same set of lists (inner order preserved)."""
    def validate(self, actual, expected, inputs=None):
        try:
            a=sorted(tuple(x) for x in actual); e=sorted(tuple(x) for x in expected)
            passed=a==e
        except Exception: passed=False; a,e=actual,expected
        return ValidationResult(passed,repr(e),repr(a),"" if passed else "Combinations differ")


# LC 78 — Subsets
class SubsetsPlugin(ProblemPlugin):
    problem_id="subsets"; leetcode_number=78; title="Subsets"; slug="subsets"
    method_name="subsets"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking","Bit Manipulation"]; parameters=["nums: List[int]"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Return all possible subsets (power set)."

    def get_test_cases(self):
        return [TestCase({"nums":[1,2,3]},[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]],"Example 1"),
                TestCase({"nums":[0]},[[],[0]],"Example 2"),
                TestCase({"nums":[1,2]},[[],[1],[2],[1,2]],"Two elements",is_hidden=True)]

    def get_validator(self): return UnorderedSubsetValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; result=[[]]
        for n in nums: result+=[s+[n] for s in result]
        return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":list(set(rng.randint(1,9) for _ in range(rng.randint(2,5))))} for _ in range(count)]


# LC 39 — Combination Sum
class CombinationSumPlugin(ProblemPlugin):
    problem_id="combination-sum"; leetcode_number=39; title="Combination Sum"; slug="combination-sum"
    method_name="combinationSum"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking"]; parameters=["candidates: List[int]","target: int"]
    return_type="List[List[int]]"; hidden_test_count=4
    description="Return all combinations of candidates that sum to target (reuse allowed)."

    def get_test_cases(self):
        return [TestCase({"candidates":[2,3,6,7],"target":7},[[2,2,3],[7]],"Example 1"),
                TestCase({"candidates":[2,3,5],"target":8},[[2,2,2,2],[2,3,3],[3,5]],"Example 2"),
                TestCase({"candidates":[2],"target":1},[],"No solution"),
                TestCase({"candidates":[1],"target":2},[[1,1]],"Simple",is_hidden=True)]

    def get_validator(self): return UnorderedSubsetValidator()

    @staticmethod
    def oracle(inputs):
        candidates,target=sorted(inputs["candidates"]),inputs["target"]
        result=[]
        def bt(start,cur,rem):
            if rem==0: result.append(cur[:]); return
            for i in range(start,len(candidates)):
                if candidates[i]>rem: break
                cur.append(candidates[i]); bt(i,cur,rem-candidates[i]); cur.pop()
        bt(0,[],target); return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            candidates=sorted(set(rng.randint(2,8) for _ in range(rng.randint(2,5))))
            target=rng.randint(5,12)
            tests.append({"candidates":candidates,"target":target})
        return tests


# LC 40 — Combination Sum II
class CombinationSumIIPlugin(ProblemPlugin):
    problem_id="combination-sum-ii"; leetcode_number=40; title="Combination Sum II"; slug="combination-sum-ii"
    method_name="combinationSum2"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking"]; parameters=["candidates: List[int]","target: int"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Find all unique combinations that sum to target (each used once)."

    def get_test_cases(self):
        return [TestCase({"candidates":[10,1,2,7,6,1,5],"target":8},[[1,1,6],[1,2,5],[1,7],[2,6]],"Example 1"),
                TestCase({"candidates":[2,5,2,1,2],"target":5},[[1,2,2],[5]],"Example 2")]

    def get_validator(self): return UnorderedSubsetValidator()

    @staticmethod
    def oracle(inputs):
        candidates,target=sorted(inputs["candidates"]),inputs["target"]
        result=[]
        def bt(start,cur,rem):
            if rem==0: result.append(cur[:]); return
            for i in range(start,len(candidates)):
                if candidates[i]>rem: break
                if i>start and candidates[i]==candidates[i-1]: continue
                cur.append(candidates[i]); bt(i+1,cur,rem-candidates[i]); cur.pop()
        bt(0,[],target); return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            candidates=[rng.randint(1,10) for _ in range(rng.randint(4,8))]
            target=rng.randint(4,10)
            tests.append({"candidates":candidates,"target":target})
        return tests


# LC 46 — Permutations
class PermutationsPlugin(ProblemPlugin):
    problem_id="permutations"; leetcode_number=46; title="Permutations"; slug="permutations"
    method_name="permute"; difficulty="Medium"; pattern="Backtracking"
    topics=["Array","Backtracking"]; parameters=["nums: List[int]"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Return all possible permutations of distinct integers."

    def get_test_cases(self):
        return [TestCase({"nums":[1,2,3]},[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]],"Example 1"),
                TestCase({"nums":[0,1]},[[0,1],[1,0]],"Example 2"),TestCase({"nums":[1]},[[1]],"Single")]

    def get_validator(self): return UnorderedListOfListsValidator()

    @staticmethod
    def oracle(inputs):
        from itertools import permutations
        return [list(p) for p in permutations(inputs["nums"])]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":rng.sample(range(1,8),rng.randint(2,5))} for _ in range(count)]


# LC 131 — Palindrome Partitioning
class PalindromePartitioningPlugin(ProblemPlugin):
    problem_id="palindrome-partitioning"; leetcode_number=131; title="Palindrome Partitioning"
    slug="palindrome-partitioning"; method_name="partition"; difficulty="Medium"; pattern="Backtracking"
    topics=["String","Dynamic Programming","Backtracking"]; parameters=["s: str"]
    return_type="List[List[str]]"; hidden_test_count=4
    description="Return all possible palindrome partitioning of s."

    def get_test_cases(self):
        return [TestCase({"s":"aab"},[["a","a","b"],["aa","b"]],"Example 1"),
                TestCase({"s":"a"},[["a"]],"Example 2"),
                TestCase({"s":"aa"},[["a","a"],["aa"]],"Two same",is_hidden=True)]

    def get_validator(self): return UnorderedSubsetValidator()

    @staticmethod
    def oracle(inputs):
        s=inputs["s"]; result=[]
        def is_pal(x): return x==x[::-1]
        def bt(start,cur):
            if start==len(s): result.append(cur[:]); return
            for end in range(start+1,len(s)+1):
                if is_pal(s[start:end]): cur.append(s[start:end]); bt(end,cur); cur.pop()
        bt(0,[]); return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        return [{"s":"".join(rng.choices(string.ascii_lowercase[:4],k=rng.randint(2,6)))} for _ in range(count)]


# LC 17 — Letter Combinations of a Phone Number
class LetterCombinationsPlugin(ProblemPlugin):
    problem_id="letter-combinations-of-a-phone-number"; leetcode_number=17
    title="Letter Combinations of a Phone Number"; slug="letter-combinations-of-a-phone-number"
    method_name="letterCombinations"; difficulty="Medium"; pattern="Backtracking"
    topics=["Hash Table","String","Backtracking"]; parameters=["digits: str"]
    return_type="List[str]"; hidden_test_count=4; description="Return all letter combinations from phone keypad digits."

    def get_test_cases(self):
        return [TestCase({"digits":"23"},["ad","ae","af","bd","be","bf","cd","ce","cf"],"Example 1"),
                TestCase({"digits":""},[],"Empty"),TestCase({"digits":"2"},["a","b","c"],"Single digit")]

    def get_validator(self):
        from backend.execution_engine.problems._validators import SetValidator
        return SetValidator()

    @staticmethod
    def oracle(inputs):
        digits=inputs["digits"]
        if not digits: return []
        phone={"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}
        result=[""]
        for d in digits:
            result=[prev+c for prev in result for c in phone.get(d,"")]
        return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"digits":"".join(str(rng.randint(2,9)) for _ in range(rng.randint(1,3)))} for _ in range(count)]


# LC 51 — N-Queens
class NQueensPlugin(ProblemPlugin):
    problem_id="n-queens"; leetcode_number=51; title="N-Queens"; slug="n-queens"
    method_name="solveNQueens"; difficulty="Hard"; pattern="Backtracking"
    topics=["Array","Backtracking"]; parameters=["n: int"]
    return_type="List[List[str]]"; hidden_test_count=3; description="Return all distinct solutions to the n-queens puzzle."

    def get_test_cases(self):
        return [TestCase({"n":4},[".Q..","...Q","Q...","..Q."],"Example 1 (first solution)"),
                TestCase({"n":1},[["Q"]],"n=1")]

    def get_validator(self): return NQueensValidator()

    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; result=[]
        def bt(row,cols,diag1,diag2,board):
            if row==n: result.append(["".join(r) for r in board]); return
            for col in range(n):
                if col in cols or (row-col) in diag1 or (row+col) in diag2: continue
                board[row][col]='Q'
                bt(row+1,cols|{col},diag1|{row-col},diag2|{row+col},board)
                board[row][col]='.'
        bt(0,set(),set(),set(),[['.']*n for _ in range(n)])
        return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"n":rng.randint(4,6)} for _ in range(count)]

class NQueensValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # Check same count and all are valid placements
        def is_valid(board):
            n=len(board)
            for r in range(n):
                row=board[r]; col=row.index('Q') if 'Q' in row else -1
                if col==-1 or row.count('Q')!=1: return False
                for r2 in range(n):
                    if r2==r: continue
                    row2=board[r2]; col2=row2.index('Q') if 'Q' in row2 else -1
                    if col2==col or abs(r-r2)==abs(col-col2): return False
            return True
        passed=len(actual)==len(expected) and all(is_valid(b) for b in actual)
        return ValidationResult(passed,f"{len(expected)} valid boards",f"{len(actual)} boards","" if passed else "Wrong count or invalid placement")
