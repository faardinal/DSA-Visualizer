// Fibonacci with memoization — demonstrates recursive call stack and memo dict growth.

export const FIBONACCI_CODE = `def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

result = fib(4)
print(result)`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const memo = (val) => h("dict_memo", "dict", val);
const fibFrame = (frame_id, n, memoState) => f(frame_id, "fib", { n: v(n), memo: r("dict_memo") });
const modFrame = (extra = {}) => f("frame_mod", "<module>", extra);

export const fibonacciTrace = [
  // 0: call fib(4), memo empty
  { step: 0, line: 8, code: "result = fib(4)", locals: [fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 1: fib(4) calls fib(3)
  { step: 1, line: 6, code: "memo[n] = fib(n-1, memo) + fib(n-2, memo)", locals: [fibFrame("f3", 3, {}), fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 2: fib(3) calls fib(2)
  { step: 2, line: 6, code: "memo[n] = fib(n-1, memo) + fib(n-2, memo)", locals: [fibFrame("f2", 2, {}), fibFrame("f3", 3, {}), fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 3: fib(2) calls fib(1)
  { step: 3, line: 6, code: "memo[n] = fib(n-1, memo) + fib(n-2, memo)", locals: [fibFrame("f1a", 1, {}), fibFrame("f2", 2, {}), fibFrame("f3", 3, {}), fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 4: fib(1) returns 1 (base case)
  { step: 4, line: 5, code: "return n", locals: [fibFrame("f2", 2, {}), fibFrame("f3", 3, {}), fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 5: fib(2) calls fib(0)
  { step: 5, line: 6, code: "memo[n] = fib(n-1, memo) + fib(n-2, memo)", locals: [fibFrame("f0a", 0, {}), fibFrame("f2", 2, {}), fibFrame("f3", 3, {}), fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 6: fib(0) returns 0 (base case)
  { step: 6, line: 5, code: "return n", locals: [fibFrame("f2", 2, {}), fibFrame("f3", 3, {}), fibFrame("f4", 4, {}), modFrame()], globals: {}, heap: [memo({})], stdout: "" },

  // 7: fib(2) computes 1+0=1, memo[2]=1, returns
  { step: 7, line: 7, code: "return memo[n]", locals: [fibFrame("f3", 3, { "2": 1 }), fibFrame("f4", 4, { "2": 1 }), modFrame()], globals: {}, heap: [memo({ "2": 1 })], stdout: "" },

  // 8: fib(3) calls fib(1) for second operand
  { step: 8, line: 6, code: "memo[n] = fib(n-1, memo) + fib(n-2, memo)", locals: [fibFrame("f1b", 1, { "2": 1 }), fibFrame("f3", 3, { "2": 1 }), fibFrame("f4", 4, { "2": 1 }), modFrame()], globals: {}, heap: [memo({ "2": 1 })], stdout: "" },

  // 9: fib(1) returns 1
  { step: 9, line: 5, code: "return n", locals: [fibFrame("f3", 3, { "2": 1 }), fibFrame("f4", 4, { "2": 1 }), modFrame()], globals: {}, heap: [memo({ "2": 1 })], stdout: "" },

  // 10: fib(3) computes 1+1=2, memo[3]=2, returns
  { step: 10, line: 7, code: "return memo[n]", locals: [fibFrame("f4", 4, { "2": 1, "3": 2 }), modFrame()], globals: {}, heap: [memo({ "2": 1, "3": 2 })], stdout: "" },

  // 11: fib(4) calls fib(2) — memo hit!
  { step: 11, line: 4, code: "if n in memo: return memo[n]", locals: [fibFrame("f2b", 2, { "2": 1, "3": 2 }), fibFrame("f4", 4, { "2": 1, "3": 2 }), modFrame()], globals: {}, heap: [memo({ "2": 1, "3": 2 })], stdout: "" },

  // 12: fib(2) returns 1 from memo
  { step: 12, line: 4, code: "return memo[n]", locals: [fibFrame("f4", 4, { "2": 1, "3": 2 }), modFrame()], globals: {}, heap: [memo({ "2": 1, "3": 2 })], stdout: "" },

  // 13: fib(4) computes 2+1=3, memo[4]=3, returns
  { step: 13, line: 7, code: "return memo[n]", locals: [modFrame({ result: v(3) })], globals: { result: v(3) }, heap: [memo({ "2": 1, "3": 2, "4": 3 })], stdout: "" },

  // 14: print(result)
  { step: 14, line: 9, code: "print(result)", locals: [modFrame({ result: v(3) })], globals: { result: v(3) }, heap: [memo({ "2": 1, "3": 2, "4": 3 })], stdout: "3" },
];