"""Batch 4 — remaining NeetCode 250 problems (set A: arrays, strings, math)."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import (
    EqualityValidator, SortedListValidator, Validator, ValidationResult
)

# LC 9 — Palindrome Number
class PalindromeNumberPlugin(ProblemPlugin):
    problem_id="palindrome-number"; leetcode_number=9; title="Palindrome Number"
    slug="palindrome-number"; method_name="isPalindrome"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Math"]; parameters=["x: int"]; return_type="bool"; hidden_test_count=4
    description="Given an integer x, return true if x is a palindrome."
    def get_test_cases(self):
        return [TestCase({"x":121},True,"Example 1"),TestCase({"x":-121},False,"Example 2"),
                TestCase({"x":10},False,"Example 3"),TestCase({"x":0},True,"Zero",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs): s=str(inputs["x"]); return s==s[::-1]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"x":rng.choice([rng.randint(0,9999),rng.randint(-999,-1),int(str(rng.randint(1,99))+str(rng.randint(1,99))[::-1])])} for _ in range(count)]


# LC 13 — Roman to Integer
class RomanToIntegerPlugin(ProblemPlugin):
    problem_id="roman-to-integer"; leetcode_number=13; title="Roman to Integer"
    slug="roman-to-integer"; method_name="romanToInt"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Hash Table","Math","String"]; parameters=["s: str"]; return_type="int"; hidden_test_count=4
    description="Convert a Roman numeral to an integer."
    def get_test_cases(self):
        return [TestCase({"s":"III"},3,"Example 1"),TestCase({"s":"LVIII"},58,"Example 2"),
                TestCase({"s":"MCMXCIV"},1994,"Example 3"),TestCase({"s":"IV"},4,"IV",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        vals={"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
        s=inputs["s"]; result=0
        for i in range(len(s)):
            if i+1<len(s) and vals[s[i]]<vals[s[i+1]]: result-=vals[s[i]]
            else: result+=vals[s[i]]
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        nums=[rng.randint(1,3999) for _ in range(count)]
        def to_roman(n):
            vals=[(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
            r=""
            for v,sym in vals:
                while n>=v: r+=sym; n-=v
            return r
        return [{"s":to_roman(n)} for n in nums]


# LC 14 — Longest Common Prefix
class LongestCommonPrefixPlugin(ProblemPlugin):
    problem_id="longest-common-prefix"; leetcode_number=14; title="Longest Common Prefix"
    slug="longest-common-prefix"; method_name="longestCommonPrefix"; difficulty="Easy"; pattern="Array"
    topics=["String","Trie"]; parameters=["strs: List[str]"]; return_type="str"; hidden_test_count=4
    description="Write a function to find the longest common prefix string amongst an array of strings."
    def get_test_cases(self):
        return [TestCase({"strs":["flower","flow","flight"]},"fl","Example 1"),
                TestCase({"strs":["dog","racecar","car"]},"","Example 2"),
                TestCase({"strs":["a"]},"a","Single",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        strs=inputs["strs"]
        if not strs: return ""
        prefix=strs[0]
        for s in strs[1:]:
            while not s.startswith(prefix): prefix=prefix[:-1]
            if not prefix: return ""
        return prefix
    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string; tests=[]
        for _ in range(count):
            prefix="".join(rng.choices(string.ascii_lowercase[:8],k=rng.randint(0,5)))
            strs=[prefix+"".join(rng.choices(string.ascii_lowercase[:8],k=rng.randint(0,6))) for _ in range(rng.randint(1,5))]
            tests.append({"strs":strs})
        return tests


# LC 36 — Valid Sudoku
class ValidSudokuPlugin(ProblemPlugin):
    problem_id="valid-sudoku"; leetcode_number=36; title="Valid Sudoku"
    slug="valid-sudoku"; method_name="isValidSudoku"; difficulty="Medium"; pattern="Array"
    topics=["Array","Hash Table","Matrix"]; parameters=["board: List[List[str]]"]
    return_type="bool"; hidden_test_count=3
    description="Determine if a 9×9 Sudoku board is valid."
    def get_test_cases(self):
        b1=[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
        b2=[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
        return [TestCase({"board":b1},True,"Example 1"),TestCase({"board":b2},False,"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        board=inputs["board"]
        rows=[set() for _ in range(9)]; cols=[set() for _ in range(9)]; boxes=[set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                v=board[r][c]
                if v==".": continue
                b=(r//3)*3+c//3
                if v in rows[r] or v in cols[c] or v in boxes[b]: return False
                rows[r].add(v); cols[c].add(v); boxes[b].add(v)
        return True
    @staticmethod
    def generate_hidden_inputs(rng,count):
        empty=[["."]*9 for _ in range(9)]; return [{"board":[row[:] for row in empty]} for _ in range(count)]


# LC 48 — Rotate Image
class RotateImagePlugin(ProblemPlugin):
    problem_id="rotate-image"; leetcode_number=48; title="Rotate Image"
    slug="rotate-image"; method_name="rotate"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Array","Math","Matrix"]; parameters=["matrix: List[List[int]]"]
    return_type="None"; hidden_test_count=4; description="Rotate an n×n matrix 90 degrees clockwise in-place."
    def get_test_cases(self):
        return [TestCase({"matrix":[[1,2,3],[4,5,6],[7,8,9]]},[[7,4,1],[8,5,2],[9,6,3]],"Example 1"),
                TestCase({"matrix":[[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]},[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]],"Example 2"),
                TestCase({"matrix":[[1]]},[[1]],"1x1",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        m=[row[:] for row in inputs["matrix"]]; n=len(m)
        for r in range(n//2):
            for c in range(r,n-r-1):
                m[r][c],m[c][n-1-r],m[n-1-r][n-1-c],m[n-1-c][r]=m[n-1-c][r],m[r][c],m[c][n-1-r],m[n-1-r][n-1-c]
        return m
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,5); tests.append({"matrix":[[rng.randint(1,50) for _ in range(n)] for _ in range(n)]})
        return tests


# LC 54 — Spiral Matrix
class SpiralMatrixPlugin(ProblemPlugin):
    problem_id="spiral-matrix"; leetcode_number=54; title="Spiral Matrix"
    slug="spiral-matrix"; method_name="spiralOrder"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Array","Matrix","Simulation"]; parameters=["matrix: List[List[int]]"]
    return_type="List[int]"; hidden_test_count=4; description="Return all elements of the matrix in spiral order."
    def get_test_cases(self):
        return [TestCase({"matrix":[[1,2,3],[4,5,6],[7,8,9]]},[1,2,3,6,9,8,7,4,5],"Example 1"),
                TestCase({"matrix":[[1,2,3,4],[5,6,7,8],[9,10,11,12]]},[1,2,3,4,8,12,11,10,9,5,6,7],"Example 2"),
                TestCase({"matrix":[[1]]},[1],"1x1",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        matrix=inputs["matrix"]; result=[]
        if not matrix: return result
        top,bottom,left,right=0,len(matrix)-1,0,len(matrix[0])-1
        while top<=bottom and left<=right:
            result.extend(matrix[top][left:right+1]); top+=1
            for r in range(top,bottom+1): result.append(matrix[r][right])
            right-=1
            if top<=bottom: result.extend(reversed(matrix[bottom][left:right+1])); bottom-=1
            if left<=right:
                for r in range(bottom,top-1,-1): result.append(matrix[r][left])
                left+=1
        return result
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            r=rng.randint(1,5); c=rng.randint(1,5)
            tests.append({"matrix":[[rng.randint(1,50) for _ in range(c)] for _ in range(r)]})
        return tests


# LC 73 — Set Matrix Zeroes
class SetMatrixZeroesPlugin(ProblemPlugin):
    problem_id="set-matrix-zeroes"; leetcode_number=73; title="Set Matrix Zeroes"
    slug="set-matrix-zeroes"; method_name="setZeroes"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Array","Hash Table","Matrix"]; parameters=["matrix: List[List[int]]"]
    return_type="None"; hidden_test_count=4; description="Set entire row/column to 0 if a cell is 0."
    def get_test_cases(self):
        return [TestCase({"matrix":[[1,1,1],[1,0,1],[1,1,1]]},[[1,0,1],[0,0,0],[1,0,1]],"Example 1"),
                TestCase({"matrix":[[0,1,2,0],[3,4,5,2],[1,3,1,5]]},[[0,0,0,0],[0,4,5,0],[0,3,1,0]],"Example 2")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        m=[row[:] for row in inputs["matrix"]]; rows,cols=len(m),len(m[0])
        zero_rows={r for r in range(rows) for c in range(cols) if m[r][c]==0}
        zero_cols={c for r in range(rows) for c in range(cols) if m[r][c]==0}
        for r in range(rows):
            for c in range(cols):
                if r in zero_rows or c in zero_cols: m[r][c]=0
        return m
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            r=rng.randint(2,4); c=rng.randint(2,4)
            m=[[rng.randint(0,5) for _ in range(c)] for _ in range(r)]
            tests.append({"matrix":m})
        return tests


# LC 202 — Happy Number
class HappyNumberPlugin(ProblemPlugin):
    problem_id="happy-number"; leetcode_number=202; title="Happy Number"
    slug="happy-number"; method_name="isHappy"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Hash Table","Math","Two Pointers"]; parameters=["n: int"]; return_type="bool"; hidden_test_count=4
    description="Return true if n is a happy number."
    def get_test_cases(self):
        return [TestCase({"n":19},True,"Example 1"),TestCase({"n":2},False,"Example 2"),
                TestCase({"n":1},True,"n=1",is_hidden=True),TestCase({"n":7},True,"n=7",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]; seen=set()
        while n!=1 and n not in seen:
            seen.add(n); n=sum(int(d)**2 for d in str(n))
        return n==1
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"n":rng.randint(1,100)} for _ in range(count)]


# LC 66 — Plus One
class PlusOnePlugin(ProblemPlugin):
    problem_id="plus-one"; leetcode_number=66; title="Plus One"
    slug="plus-one"; method_name="plusOne"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Array","Math"]; parameters=["digits: List[int]"]; return_type="List[int]"; hidden_test_count=4
    description="Increment the large integer represented as digits array by one."
    def get_test_cases(self):
        return [TestCase({"digits":[1,2,3]},[1,2,4],"Example 1"),
                TestCase({"digits":[4,3,2,1]},[4,3,2,2],"Example 2"),
                TestCase({"digits":[9]},[1,0],"Carry"),
                TestCase({"digits":[9,9,9]},[1,0,0,0],"All nines",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        digits=list(inputs["digits"])
        for i in range(len(digits)-1,-1,-1):
            if digits[i]<9: digits[i]+=1; return digits
            digits[i]=0
        return [1]+digits
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"digits":[rng.randint(0,9) for _ in range(rng.randint(1,6))]} for _ in range(count)]


# LC 258 — Add Digits
class AddDigitsPlugin(ProblemPlugin):
    problem_id="add-digits"; leetcode_number=258; title="Add Digits"
    slug="add-digits"; method_name="addDigits"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Math","Simulation","Number Theory"]; parameters=["num: int"]; return_type="int"; hidden_test_count=4
    description="Repeatedly add all digits of num until result is a single digit."
    def get_test_cases(self):
        return [TestCase({"num":38},2,"Example 1"),TestCase({"num":0},0,"Example 2"),
                TestCase({"num":9},9,"Nine",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["num"]
        if n==0: return 0
        return 1+(n-1)%9
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"num":rng.randint(0,9999)} for _ in range(count)]


# LC 367 — Valid Perfect Square
class ValidPerfectSquarePlugin(ProblemPlugin):
    problem_id="valid-perfect-square"; leetcode_number=367; title="Valid Perfect Square"
    slug="valid-perfect-square"; method_name="isPerfectSquare"; difficulty="Easy"; pattern="Binary Search"
    topics=["Math","Binary Search"]; parameters=["num: int"]; return_type="bool"; hidden_test_count=4
    description="Return true if num is a perfect square without using sqrt."
    def get_test_cases(self):
        return [TestCase({"num":16},True,"Example 1"),TestCase({"num":14},False,"Example 2"),
                TestCase({"num":1},True,"One",is_hidden=True),TestCase({"num":4},True,"Four",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["num"]; lo,hi=1,n
        while lo<=hi:
            mid=(lo+hi)//2; sq=mid*mid
            if sq==n: return True
            elif sq<n: lo=mid+1
            else: hi=mid-1
        return False
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            if i%2==0: n=rng.randint(1,100)**2
            else: n=rng.randint(2,10000)
            tests.append({"num":n})
        return tests


# LC 412 — Fizz Buzz
class FizzBuzzPlugin(ProblemPlugin):
    problem_id="fizz-buzz"; leetcode_number=412; title="Fizz Buzz"
    slug="fizz-buzz"; method_name="fizzBuzz"; difficulty="Easy"; pattern="Math & Geometry"
    topics=["Math","String","Simulation"]; parameters=["n: int"]; return_type="List[str]"; hidden_test_count=4
    description="Return array of strings for numbers 1..n: Fizz/Buzz/FizzBuzz rules."
    def get_test_cases(self):
        return [TestCase({"n":3},["1","2","Fizz"],"Example 1"),
                TestCase({"n":5},["1","2","Fizz","4","Buzz"],"Example 2"),
                TestCase({"n":15},["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"],"Example 3")]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        n=inputs["n"]
        return ["FizzBuzz" if i%15==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else str(i) for i in range(1,n+1)]
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"n":rng.randint(1,20)} for _ in range(count)]


# LC 283 — Move Zeroes
class MoveZeroesPlugin(ProblemPlugin):
    problem_id="move-zeroes"; leetcode_number=283; title="Move Zeroes"
    slug="move-zeroes"; method_name="moveZeroes"; difficulty="Easy"; pattern="Array"
    topics=["Array","Two Pointers"]; parameters=["nums: List[int]"]; return_type="None"; hidden_test_count=4
    description="Move all zeroes to end while maintaining relative order of non-zero elements."
    def get_test_cases(self):
        return [TestCase({"nums":[0,1,0,3,12]},[1,3,12,0,0],"Example 1"),
                TestCase({"nums":[0]},[0],"Single zero"),
                TestCase({"nums":[1]},[1],"No zero",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        nums=list(inputs["nums"]); pos=0
        for i in range(len(nums)):
            if nums[i]!=0: nums[pos]=nums[i]; pos+=1
        while pos<len(nums): nums[pos]=0; pos+=1
        return nums
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.choice([0,0,rng.randint(1,9)]) for _ in range(rng.randint(2,12))]} for _ in range(count)]


# LC 349 — Intersection of Two Arrays
class IntersectionTwoArraysPlugin(ProblemPlugin):
    problem_id="intersection-of-two-arrays"; leetcode_number=349; title="Intersection of Two Arrays"
    slug="intersection-of-two-arrays"; method_name="intersection"; difficulty="Easy"; pattern="Array"
    topics=["Array","Hash Table","Two Pointers","Binary Search","Sorting"]
    parameters=["nums1: List[int]","nums2: List[int]"]; return_type="List[int]"; hidden_test_count=4
    description="Return the intersection of two arrays (unique elements)."
    def get_test_cases(self):
        return [TestCase({"nums1":[1,2,2,1],"nums2":[2,2]},[2],"Example 1"),
                TestCase({"nums1":[4,9,5],"nums2":[9,4,9,8,4]},[9,4],"Example 2")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import SetValidator; return SetValidator()
    @staticmethod
    def oracle(inputs):
        return list(set(inputs["nums1"]) & set(inputs["nums2"]))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n1=[rng.randint(1,10) for _ in range(rng.randint(2,8))]
            n2=[rng.randint(1,10) for _ in range(rng.randint(2,8))]
            tests.append({"nums1":n1,"nums2":n2})
        return tests


# LC 350 — Intersection of Two Arrays II
class IntersectionTwoArraysIIPlugin(ProblemPlugin):
    problem_id="intersection-of-two-arrays-ii"; leetcode_number=350; title="Intersection of Two Arrays II"
    slug="intersection-of-two-arrays-ii"; method_name="intersect"; difficulty="Easy"; pattern="Array"
    topics=["Array","Hash Table","Two Pointers","Binary Search","Sorting"]
    parameters=["nums1: List[int]","nums2: List[int]"]; return_type="List[int]"; hidden_test_count=4
    description="Return intersection including duplicates."
    def get_test_cases(self):
        return [TestCase({"nums1":[1,2,2,1],"nums2":[2,2]},[2,2],"Example 1"),
                TestCase({"nums1":[4,9,5],"nums2":[9,4,9,8,4]},[4,9],"Example 2")]
    def get_validator(self):
        from backend.execution_engine.problems._validators import SortedListValidator; return SortedListValidator()
    @staticmethod
    def oracle(inputs):
        from collections import Counter; c1,c2=Counter(inputs["nums1"]),Counter(inputs["nums2"])
        return sorted(k for k in c1 for _ in range(min(c1[k],c2.get(k,0))))
    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n1=[rng.randint(1,8) for _ in range(rng.randint(2,8))]
            n2=[rng.randint(1,8) for _ in range(rng.randint(2,8))]
            tests.append({"nums1":n1,"nums2":n2})
        return tests


# LC 119 — Pascal's Triangle II
class PascalsTriangleIIPlugin(ProblemPlugin):
    problem_id="pascals-triangle-ii"; leetcode_number=119; title="Pascal's Triangle II"
    slug="pascals-triangle-ii"; method_name="getRow"; difficulty="Easy"; pattern="Array"
    topics=["Array","Dynamic Programming"]; parameters=["rowIndex: int"]; return_type="List[int]"; hidden_test_count=4
    description="Return the rowIndex-th (0-indexed) row of Pascal's triangle."
    def get_test_cases(self):
        return [TestCase({"rowIndex":3},[1,3,3,1],"Example 1"),TestCase({"rowIndex":0},[1],"Example 2"),
                TestCase({"rowIndex":1},[1,1],"Example 3"),TestCase({"rowIndex":4},[1,4,6,4,1],"Row 4",is_hidden=True)]
    def get_validator(self): return EqualityValidator()
    @staticmethod
    def oracle(inputs):
        k=inputs["rowIndex"]; row=[1]*(k+1)
        for i in range(1,k):
            for j in range(i,0,-1): row[j]+=row[j-1]
        return row
    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"rowIndex":rng.randint(0,15)} for _ in range(count)]
