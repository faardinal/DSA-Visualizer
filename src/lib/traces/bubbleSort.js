// Bubble Sort trace — demonstrates swap animations on an in-place array.

export const BUBBLE_SORT_CODE = `def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

arr = [4, 2, 3, 1]
result = bubble_sort(arr)
print(result)`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const mod = (extra = {}) => f("frame_mod", "<module>", { arr: r("list_arr"), ...extra });
const fn = (arrVal, extra = {}) => f("frame_fn", "bubble_sort", { arr: r("list_arr"), ...extra });

const G = { arr: r("list_arr") };

export const bubbleSortTrace = [
  { step: 0, line: 9, code: "arr = [4, 2, 3, 1]", locals: [mod()], globals: { arr: r("list_arr") }, heap: [h("list_arr", "list", [4, 2, 3, 1])], stdout: "" },
  { step: 1, line: 10, code: "result = bubble_sort(arr)", locals: [fn([4, 2, 3, 1]), mod()], globals: G, heap: [h("list_arr", "list", [4, 2, 3, 1])], stdout: "" },
  { step: 2, line: 2, code: "n = len(arr)", locals: [fn([4, 2, 3, 1], { n: v(4) }), mod()], globals: G, heap: [h("list_arr", "list", [4, 2, 3, 1])], stdout: "" },
  { step: 3, line: 4, code: "for i in range(n):", locals: [fn([4, 2, 3, 1], { n: v(4), i: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [4, 2, 3, 1])], stdout: "" },
  { step: 4, line: 5, code: "for j in range(0, n - i - 1):", locals: [fn([4, 2, 3, 1], { n: v(4), i: v(0), j: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [4, 2, 3, 1])], stdout: "" },
  { step: 5, line: 6, code: "arr[j], arr[j+1] = arr[j+1], arr[j]", locals: [fn([2, 4, 3, 1], { n: v(4), i: v(0), j: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 4, 3, 1])], stdout: "" },
  { step: 6, line: 5, code: "for j in range(0, n - i - 1):", locals: [fn([2, 4, 3, 1], { n: v(4), i: v(0), j: v(1) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 4, 3, 1])], stdout: "" },
  { step: 7, line: 6, code: "arr[j], arr[j+1] = arr[j+1], arr[j]", locals: [fn([2, 3, 4, 1], { n: v(4), i: v(0), j: v(1) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 3, 4, 1])], stdout: "" },
  { step: 8, line: 5, code: "for j in range(0, n - i - 1):", locals: [fn([2, 3, 4, 1], { n: v(4), i: v(0), j: v(2) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 3, 4, 1])], stdout: "" },
  { step: 9, line: 6, code: "arr[j], arr[j+1] = arr[j+1], arr[j]", locals: [fn([2, 3, 1, 4], { n: v(4), i: v(0), j: v(2) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 3, 1, 4])], stdout: "" },
  { step: 10, line: 4, code: "for i in range(n):", locals: [fn([2, 3, 1, 4], { n: v(4), i: v(1) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 3, 1, 4])], stdout: "" },
  { step: 11, line: 5, code: "for j in range(0, n - i - 1):", locals: [fn([2, 3, 1, 4], { n: v(4), i: v(1), j: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 3, 1, 4])], stdout: "" },
  { step: 12, line: 5, code: "for j in range(0, n - i - 1):", locals: [fn([2, 3, 1, 4], { n: v(4), i: v(1), j: v(1) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 3, 1, 4])], stdout: "" },
  { step: 13, line: 6, code: "arr[j], arr[j+1] = arr[j+1], arr[j]", locals: [fn([2, 1, 3, 4], { n: v(4), i: v(1), j: v(1) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 1, 3, 4])], stdout: "" },
  { step: 14, line: 4, code: "for i in range(n):", locals: [fn([2, 1, 3, 4], { n: v(4), i: v(2) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 1, 3, 4])], stdout: "" },
  { step: 15, line: 5, code: "for j in range(0, n - i - 1):", locals: [fn([2, 1, 3, 4], { n: v(4), i: v(2), j: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [2, 1, 3, 4])], stdout: "" },
  { step: 16, line: 6, code: "arr[j], arr[j+1] = arr[j+1], arr[j]", locals: [fn([1, 2, 3, 4], { n: v(4), i: v(2), j: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [1, 2, 3, 4])], stdout: "" },
  { step: 17, line: 8, code: "return arr", locals: [fn([1, 2, 3, 4], { n: v(4), i: v(2), j: v(0) }), mod()], globals: G, heap: [h("list_arr", "list", [1, 2, 3, 4])], stdout: "" },
  { step: 18, line: 10, code: "result = bubble_sort(arr)", locals: [mod({ result: r("list_arr") })], globals: { ...G, result: r("list_arr") }, heap: [h("list_arr", "list", [1, 2, 3, 4])], stdout: "" },
  { step: 19, line: 11, code: "print(result)", locals: [mod({ result: r("list_arr") })], globals: { ...G, result: r("list_arr") }, heap: [h("list_arr", "list", [1, 2, 3, 4])], stdout: "[1, 2, 3, 4]" },
];