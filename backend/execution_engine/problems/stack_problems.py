"""Stack pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult


# ---------------------------------------------------------------------------
# Min Stack  (LC 155) — stateful design
# ---------------------------------------------------------------------------
_MIN_STACK_WRAPPER = '''
{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = MinStack()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "push":
            obj.push(arg[0])
            out.append(None)
        elif op == "pop":
            obj.pop()
            out.append(None)
        elif op == "top":
            out.append(obj.top())
        elif op == "getMin":
            out.append(obj.getMin())
        else:
            out.append(None)
    print("__RESULT__:")
    print(repr(out))

main()
'''

class MinStackPlugin(ProblemPlugin):
    problem_id = "min-stack"
    leetcode_number = 155
    slug = "min-stack"
    title = "Min Stack"
    method_name = "push"
    difficulty = "Medium"
    pattern = "Stack"
    topics = ["Stack", "Design"]
    parameters = ["val: int"]
    return_type = "None"
    hidden_test_count = 3
    stateful = True
    description = (
        "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time."
    )

    def get_test_cases(self):
        return [
            TestCase(
                {"ops": ["MinStack","push","push","push","getMin","pop","top","getMin"],
                 "args": [[], [-3], [0], [-2], [], [], [], []]},
                [None,None,None,None,-3,None,0,-2],
                "Example 1"
            ),
            TestCase(
                {"ops": ["MinStack","push","push","getMin","pop","getMin"],
                 "args": [[], [5], [3], [], [], []]},
                [None,None,None,3,None,5],
                "Hidden: pop reveals prev min", is_hidden=True
            ),
        ]

    def get_validator(self): return EqualityValidator()

    def get_wrapper_template(self):
        return WrapperTemplate(template_str=_MIN_STACK_WRAPPER)

    @staticmethod
    def oracle(inputs):
        ops, args = inputs["ops"], inputs["args"]
        stack = []
        min_stack = []
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "push":
                v = arg[0]
                stack.append(v)
                min_stack.append(min(v, min_stack[-1] if min_stack else v))
                out.append(None)
            elif op == "pop":
                stack.pop(); min_stack.pop()
                out.append(None)
            elif op == "top":
                out.append(stack[-1])
            elif op == "getMin":
                out.append(min_stack[-1])
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            ops = ["MinStack"]
            args = [[]]
            vals = [rng.randint(-50, 50) for _ in range(rng.randint(3, 8))]
            for v in vals:
                ops.append("push"); args.append([v])
            for _ in range(rng.randint(1, 3)):
                ops.append("getMin"); args.append([])
                if len(vals) > 1:
                    ops.append("pop"); args.append([])
                    vals.pop()
                    ops.append("getMin"); args.append([])
            tests.append({"ops": ops, "args": args})
        return tests


# ---------------------------------------------------------------------------
# Evaluate Reverse Polish Notation  (LC 150)
# ---------------------------------------------------------------------------
class EvalRPNPlugin(ProblemPlugin):
    problem_id = "evaluate-reverse-polish-notation"
    leetcode_number = 150
    slug = "evaluate-reverse-polish-notation"
    title = "Evaluate Reverse Polish Notation"
    method_name = "evalRPN"
    difficulty = "Medium"
    pattern = "Stack"
    topics = ["Array", "Math", "Stack"]
    parameters = ["tokens: List[str]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Evaluate the value of an arithmetic expression in Reverse Polish Notation."
    )

    def get_test_cases(self):
        return [
            TestCase({"tokens": ["2","1","+","3","*"]}, 9, "Example 1"),
            TestCase({"tokens": ["4","13","5","/","+"]}, 6, "Example 2"),
            TestCase({"tokens": ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]}, 22, "Example 3"),
            TestCase({"tokens": ["3","4","+"]}, 7, "Simple add", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        stack = []
        for t in inputs["tokens"]:
            if t in "+-*/":
                b, a = stack.pop(), stack.pop()
                if t == "+": stack.append(a + b)
                elif t == "-": stack.append(a - b)
                elif t == "*": stack.append(a * b)
                else: stack.append(int(a / b))
            else:
                stack.append(int(t))
        return stack[0]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            a, b, c = rng.randint(1,20), rng.randint(1,20), rng.randint(1,5)
            op1, op2 = rng.choice(["+","-","*"]), rng.choice(["+","-"])
            tests.append({"tokens": [str(a), str(b), op1, str(c), op2]})
        return tests


# ---------------------------------------------------------------------------
# Generate Parentheses  (LC 22)
# ---------------------------------------------------------------------------
class GenerateParenthesesPlugin(ProblemPlugin):
    problem_id = "generate-parentheses"
    leetcode_number = 22
    slug = "generate-parentheses"
    title = "Generate Parentheses"
    method_name = "generateParenthesis"
    difficulty = "Medium"
    pattern = "Stack"
    topics = ["String", "Dynamic Programming", "Backtracking"]
    parameters = ["n: int"]
    return_type = "List[str]"
    hidden_test_count = 3
    description = "Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses."

    def get_test_cases(self):
        return [
            TestCase({"n": 3}, ["((()))","(()())","(())()","()(())","()()()"], "Example 1"),
            TestCase({"n": 1}, ["()"], "Example 2"),
            TestCase({"n": 2}, ["(())", "()()"], "n=2", is_hidden=True),
        ]

    def get_validator(self):
        from backend.execution_engine.problems._validators import SetValidator
        return SetValidator()

    @staticmethod
    def oracle(inputs):
        n = inputs["n"]
        result = []
        def bt(s, o, c):
            if len(s) == 2*n: result.append(s); return
            if o < n: bt(s+"(", o+1, c)
            if c < o: bt(s+")", o, c+1)
        bt("", 0, 0)
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        return [{"n": rng.randint(1, 4)} for _ in range(count)]


# ---------------------------------------------------------------------------
# Daily Temperatures  (LC 739)
# ---------------------------------------------------------------------------
class DailyTemperaturesPlugin(ProblemPlugin):
    problem_id = "daily-temperatures"
    leetcode_number = 739
    slug = "daily-temperatures"
    title = "Daily Temperatures"
    method_name = "dailyTemperatures"
    difficulty = "Medium"
    pattern = "Stack"
    topics = ["Array", "Stack", "Monotonic Stack"]
    parameters = ["temperatures: List[int]"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = (
        "Given an array of integers temperatures represents the daily temperatures, "
        "return an array such that answer[i] is the number of days you have to wait after the ith day "
        "to get a warmer temperature."
    )

    def get_test_cases(self):
        return [
            TestCase({"temperatures": [73,74,75,71,69,72,76,73]}, [1,1,4,2,1,1,0,0], "Example 1"),
            TestCase({"temperatures": [30,40,50,60]}, [1,1,1,0], "Example 2"),
            TestCase({"temperatures": [30,60,90]}, [1,1,0], "Example 3"),
            TestCase({"temperatures": [89,62,70,58,47,47,46,76,100,70]}, [8,1,5,4,3,2,1,1,0,0], "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        temps = inputs["temperatures"]
        result = [0] * len(temps)
        stack = []
        for i, t in enumerate(temps):
            while stack and temps[stack[-1]] < t:
                j = stack.pop()
                result[j] = i - j
            stack.append(i)
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(3, 15)
            tests.append({"temperatures": [rng.randint(30, 100) for _ in range(n)]})
        return tests


# ---------------------------------------------------------------------------
# Car Fleet  (LC 853)
# ---------------------------------------------------------------------------
class CarFleetPlugin(ProblemPlugin):
    problem_id = "car-fleet"
    leetcode_number = 853
    slug = "car-fleet"
    title = "Car Fleet"
    method_name = "carFleet"
    difficulty = "Medium"
    pattern = "Stack"
    topics = ["Array", "Stack", "Sorting", "Monotonic Stack"]
    parameters = ["target: int", "position: List[int]", "speed: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "There are n cars going to the same destination along a one-lane road. "
        "A car fleet is some non-empty set of cars driving at the same position and speed. "
        "Return the number of car fleets that will arrive at the destination."
    )

    def get_test_cases(self):
        return [
            TestCase({"target": 12, "position": [10,8,0,5,3], "speed": [2,4,1,1,3]}, 3, "Example 1"),
            TestCase({"target": 10, "position": [3], "speed": [3]}, 1, "Example 2"),
            TestCase({"target": 100, "position": [0,2,4], "speed": [4,2,1]}, 1, "Example 3"),
            TestCase({"target": 10, "position": [6,8], "speed": [3,2]}, 2, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        target = inputs["target"]
        pairs = sorted(zip(inputs["position"], inputs["speed"]), reverse=True)
        stack = []
        for pos, spd in pairs:
            t = (target - pos) / spd
            if not stack or t > stack[-1]:
                stack.append(t)
        return len(stack)

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 10)
            target = rng.randint(20, 100)
            positions = rng.sample(range(target), min(n, target))
            speeds = [rng.randint(1, 10) for _ in range(len(positions))]
            tests.append({"target": target, "position": positions, "speed": speeds})
        return tests


# ---------------------------------------------------------------------------
# Largest Rectangle in Histogram  (LC 84)
# ---------------------------------------------------------------------------
class LargestRectangleHistogramPlugin(ProblemPlugin):
    problem_id = "largest-rectangle-in-histogram"
    leetcode_number = 84
    slug = "largest-rectangle-in-histogram"
    title = "Largest Rectangle in Histogram"
    method_name = "largestRectangleArea"
    difficulty = "Hard"
    pattern = "Stack"
    topics = ["Array", "Stack", "Monotonic Stack"]
    parameters = ["heights: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "Given an array of integers heights representing the histogram's bar height "
        "where the width of each bar is 1, return the area of the largest rectangle in the histogram."
    )

    def get_test_cases(self):
        return [
            TestCase({"heights": [2,1,5,6,2,3]}, 10, "Example 1"),
            TestCase({"heights": [2,4]}, 4, "Example 2"),
            TestCase({"heights": [1]}, 1, "Single bar", is_hidden=True),
            TestCase({"heights": [6,2,5,4,5,1,6]}, 12, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        heights = inputs["heights"] + [0]
        stack = [-1]
        best = 0
        for i, h in enumerate(heights):
            while stack[-1] != -1 and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                width = i - stack[-1] - 1
                best = max(best, height * width)
            stack.append(i)
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 15)
            tests.append({"heights": [rng.randint(1, 20) for _ in range(n)]})
        return tests
