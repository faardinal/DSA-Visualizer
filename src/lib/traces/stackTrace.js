// Stack trace — demonstrates push (slide from top) and pop (fade upward).

export const STACK_CODE = `stack = []
stack.append(10)
stack.append(20)
stack.append(30)
val = stack.pop()
print(val)`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const mod = (extra = {}) => f("frame_mod", "<module>", extra);
const G = {};

export const stackTrace = [
  { step: 0, line: 1, code: "stack = []", locals: [mod({ stack: r("stack_s") })], globals: { ...G, stack: r("stack_s") }, heap: [h("stack_s", "stack", [])], stdout: "" },
  { step: 1, line: 2, code: "stack.append(10)", locals: [mod({ stack: r("stack_s") })], globals: { ...G, stack: r("stack_s") }, heap: [h("stack_s", "stack", [10])], stdout: "" },
  { step: 2, line: 3, code: "stack.append(20)", locals: [mod({ stack: r("stack_s") })], globals: { ...G, stack: r("stack_s") }, heap: [h("stack_s", "stack", [10, 20])], stdout: "" },
  { step: 3, line: 4, code: "stack.append(30)", locals: [mod({ stack: r("stack_s") })], globals: { ...G, stack: r("stack_s") }, heap: [h("stack_s", "stack", [10, 20, 30])], stdout: "" },
  { step: 4, line: 5, code: "val = stack.pop()", locals: [mod({ stack: r("stack_s"), val: v(30) })], globals: { ...G, stack: r("stack_s"), val: v(30) }, heap: [h("stack_s", "stack", [10, 20])], stdout: "" },
  { step: 5, line: 6, code: "print(val)", locals: [mod({ stack: r("stack_s"), val: v(30) })], globals: { ...G, stack: r("stack_s"), val: v(30) }, heap: [h("stack_s", "stack", [10, 20])], stdout: "30" },
];