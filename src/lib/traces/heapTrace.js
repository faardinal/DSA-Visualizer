// Heap heapify trace — demonstrates parent-child swaps during heapify.
// Heap stored as array (same as list), rendered as binary tree.

export const HEAP_CODE = `import heapq
arr = [4, 10, 3, 5, 1]
heapq.heapify(arr)
print(arr)`;

function r(id) {
  return { ref: id };
}

function v(val) {
  return { value: val };
}

function h(id, type, value) {
  return { id, type, value };
}

function f(frame_id, func, vars) {
  return { frame_id, func, vars };
}

function mod(extra) {
  if (!extra) extra = {};
  return f("frame_mod", "<module>", extra);
}

export const heapTrace = [
  {
    step: 0,
    line: 2,
    code: "arr = [4, 10, 3, 5, 1]",
    locals: [mod({ arr: r("heap_h") })],
    globals: { arr: r("heap_h") },
    heap: [h("heap_h", "heap", [4, 10, 3, 5, 1])],
    stdout: "",
  },
  {
    step: 1,
    line: 3,
    code: "heapq.heapify(arr)",
    locals: [mod({ arr: r("heap_h") })],
    globals: { arr: r("heap_h") },
    heap: [h("heap_h", "heap", [4, 1, 3, 5, 10])],
    stdout: "",
  },
  {
    step: 2,
    line: 3,
    code: "heapq.heapify(arr)",
    locals: [mod({ arr: r("heap_h") })],
    globals: { arr: r("heap_h") },
    heap: [h("heap_h", "heap", [1, 4, 3, 5, 10])],
    stdout: "",
  },
  {
    step: 3,
    line: 3,
    code: "heapq.heapify(arr)",
    locals: [mod({ arr: r("heap_h") })],
    globals: { arr: r("heap_h") },
    heap: [h("heap_h", "heap", [1, 4, 3, 5, 10])],
    stdout: "",
  },
  {
    step: 4,
    line: 4,
    code: "print(arr)",
    locals: [mod({ arr: r("heap_h") })],
    globals: { arr: r("heap_h") },
    heap: [h("heap_h", "heap", [1, 4, 3, 5, 10])],
    stdout: "[1, 4, 3, 5, 10]",
  },
];