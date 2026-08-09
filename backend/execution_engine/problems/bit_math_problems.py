"""Bit Manipulation & Math pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator


# LC 191 — Number of 1 Bits
class NumberOf1BitsPlugin(ProblemPlugin):
    problem_id="number-of-1-bits"; leetcode_number=191; title="Number of 1 Bits"; slug="number-of-1-bits"
    method_name="hammingWeight"; difficulty="Easy"; pattern="Bit Manipulation"
    topics=["Divide and Conquer","Bit Manipulation"]; parameters=["n: int"]
    return_type="int"; hidden_test_count=4; description="Return number of set bits in the binary representation of n."

    def get_test_cases(self):
        return [TestCase({"n":11},3,"Example 1: 1011"),TestCase({"n":128},1,"Example 2: 10000000"),
                TestCase({"n":2147483645},30,"Example 3"),TestCase({"n":0},0,"Zero",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs): return bin(inputs["n"]).count('1')

    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,2**31-1)} for _ in range(count)]


# LC 338 — Counting Bits
class CountingBitsPlugin(ProblemPlugin):
    problem_id="counting-bits"; leetcode_number=338; title="Counting Bits"; slug="counting-bits"
    method_name="countBits"; difficulty="Easy"; pattern="Bit Manipulation"
    topics=["Dynamic Programming","Bit Manipulation"]; parameters=["n: int"]
    return_type="List[int]"; hidden_test_count=4; description="Return array ans where ans[i] = number of 1s in binary representation of i."

    def get_test_cases(self):
        return [TestCase({"n":2},[0,1,1],"Example 1"),TestCase({"n":5},[0,1,1,2,1,2],"Example 2"),
                TestCase({"n":0},[0],"Zero",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs): return [bin(i).count('1') for i in range(inputs["n"]+1)]

    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,100)} for _ in range(count)]


# LC 190 — Reverse Bits
class ReverseBitsPlugin(ProblemPlugin):
    problem_id="reverse-bits"; leetcode_number=190; title="Reverse Bits"; slug="reverse-bits"
    method_name="reverseBits"; difficulty="Easy"; pattern="Bit Manipulation"
    topics=["Divide and Conquer","Bit Manipulation"]; parameters=["n: int"]
    return_type="int"; hidden_test_count=4; description="Reverse bits of a 32-bit unsigned integer."

    def get_test_cases(self):
        return [TestCase({"n":43261596},964176192,"Example 1"),TestCase({"n":4294967293},3221225471,"Example 2"),
                TestCase({"n":0},0,"Zero",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs): return int(bin(inputs["n"])[2:].zfill(32)[::-1],2)

    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"n":rng.randint(0,2**32-1)} for _ in range(count)]


# LC 268 — Missing Number
class MissingNumberPlugin(ProblemPlugin):
    problem_id="missing-number"; leetcode_number=268; title="Missing Number"; slug="missing-number"
    method_name="missingNumber"; difficulty="Easy"; pattern="Bit Manipulation"
    topics=["Array","Hash Table","Math","Bit Manipulation","Sorting"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4; description="Given array containing n distinct numbers in [0,n], return the missing number."

    def get_test_cases(self):
        return [TestCase({"nums":[3,0,1]},2,"Example 1"),TestCase({"nums":[0,1]},2,"Example 2"),
                TestCase({"nums":[9,6,4,2,3,5,7,0,1]},8,"Example 3"),
                TestCase({"nums":[0]},1,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; n=len(nums)
        return n*(n+1)//2-sum(nums)

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(1,15); nums=list(range(n+1)); rng.shuffle(nums)
            missing=nums.pop(rng.randint(0,len(nums)-1)); tests.append({"nums":nums})
        return tests


# LC 136 — Single Number
class SingleNumberPlugin(ProblemPlugin):
    problem_id="single-number"; leetcode_number=136; title="Single Number"; slug="single-number"
    method_name="singleNumber"; difficulty="Easy"; pattern="Bit Manipulation"
    topics=["Array","Bit Manipulation"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4; description="Return the element that appears only once (every other appears twice)."

    def get_test_cases(self):
        return [TestCase({"nums":[2,2,1]},1,"Example 1"),TestCase({"nums":[4,1,2,1,2]},4,"Example 2"),
                TestCase({"nums":[1]},1,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        result=0
        for n in inputs["nums"]: result^=n
        return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            unique=rng.randint(-50,50)
            pairs=[rng.randint(-50,50) for _ in range(rng.randint(1,6))]
            nums=[unique]+pairs+pairs; rng.shuffle(nums); tests.append({"nums":nums})
        return tests


# LC 7 — Reverse Integer
class ReverseIntegerPlugin(ProblemPlugin):
    problem_id="reverse-integer"; leetcode_number=7; title="Reverse Integer"; slug="reverse-integer"
    method_name="reverse"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math"]; parameters=["x: int"]
    return_type="int"; hidden_test_count=4; description="Reverse digits of a 32-bit signed integer. Return 0 if overflow."

    def get_test_cases(self):
        return [TestCase({"x":123},321,"Example 1"),TestCase({"x":-123},-321,"Example 2"),
                TestCase({"x":120},21,"Example 3"),TestCase({"x":0},0,"Zero",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        x=inputs["x"]; sign=1 if x>=0 else -1; r=int(str(abs(x))[::-1])*sign
        return r if -(2**31)<=r<=2**31-1 else 0

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"x":rng.randint(-2**31,2**31-1)} for _ in range(count)]


# LC 50 — Pow(x, n)
class PowPlugin(ProblemPlugin):
    problem_id="powx-n"; leetcode_number=50; title="Pow(x, n)"; slug="powx-n"
    method_name="myPow"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math","Recursion"]; parameters=["x: float","n: int"]
    return_type="float"; hidden_test_count=4; description="Implement pow(x, n)."

    def get_test_cases(self):
        return [TestCase({"x":2.0,"n":10},1024.0,"Example 1"),TestCase({"x":2.1,"n":3},9.261,"Example 2"),
                TestCase({"x":2.0,"n":-2},0.25,"Negative exp"),TestCase({"x":1.0,"n":100},1.0,"Base 1",is_hidden=True)]

    def get_validator(self):
        from backend.execution_engine.problems._validators import FloatValidator
        return FloatValidator(tol=1e-4)

    @staticmethod
    def oracle(inputs): return inputs["x"]**inputs["n"]

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"x":round(rng.uniform(0.5,3.0),2),"n":rng.randint(-5,10)} for _ in range(count)]


# LC 371 — Sum of Two Integers (bit manipulation, no + or -)
class SumTwoIntegersPlugin(ProblemPlugin):
    problem_id="sum-of-two-integers"; leetcode_number=371; title="Sum of Two Integers"; slug="sum-of-two-integers"
    method_name="getSum"; difficulty="Medium"; pattern="Bit Manipulation"
    topics=["Math","Bit Manipulation"]; parameters=["a: int","b: int"]
    return_type="int"; hidden_test_count=4; description="Calculate sum of two integers without using + or -."

    def get_test_cases(self):
        return [TestCase({"a":1,"b":2},3,"Example 1"),TestCase({"a":2,"b":3},5,"Example 2"),
                TestCase({"a":0,"b":0},0,"Both zero",is_hidden=True),TestCase({"a":-1,"b":1},0,"Neg+pos",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs): return inputs["a"]+inputs["b"]

    @staticmethod
    def generate_hidden_inputs(rng,count): return [{"a":rng.randint(-50,50),"b":rng.randint(-50,50)} for _ in range(count)]


# LC 43 — Multiply Strings
class MultiplyStringsPlugin(ProblemPlugin):
    problem_id="multiply-strings"; leetcode_number=43; title="Multiply Strings"; slug="multiply-strings"
    method_name="multiply"; difficulty="Medium"; pattern="Math & Geometry"
    topics=["Math","String","Simulation"]; parameters=["num1: str","num2: str"]
    return_type="str"; hidden_test_count=4; description="Given two non-negative integers as strings, return their product as a string."

    def get_test_cases(self):
        return [TestCase({"num1":"2","num2":"3"},"6","Example 1"),TestCase({"num1":"123","num2":"456"},"56088","Example 2"),
                TestCase({"num1":"0","num2":"123"},"0","Zero",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs): return str(int(inputs["num1"])*int(inputs["num2"]))

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"num1":str(rng.randint(0,9999)),"num2":str(rng.randint(0,9999))} for _ in range(count)]
