// Binary Search trace — demonstrates left/right/mid pointers on an array.

export const BINARY_SEARCH_CODE = `def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

arr = [1, 3, 5, 7, 9, 11]
result = binary_search(arr, 7)
print(result)`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const ARR = [1, 3, 5, 7, 9, 11];
const arrHeap = () => h("list_arr", "list", [...ARR]);

const mod = (extra = {}) => f("frame_mod", "<module>", { arr: r("list_arr"), ...extra });
const fn = (extra = {}) => f("frame_fn", "binary_search", { arr: r("list_arr"), target: v(7), ...extra });

const G = { arr: r("list_arr") };

export const binarySearchTrace = [
  { step: 0, line: 13, code: "arr = [1, 3, 5, 7, 9, 11]", locals: [mod()], globals: { arr: r("list_arr") }, heap: [arrHeap()], stdout: "" },
  { step: 1, line: 14, code: "result = binary_search(arr, 7)", locals: [mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 2, line: 2, code: "left = 0", locals: [fn({ left: v(0) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 3, line: 3, code: "right = len(arr) - 1", locals: [fn({ left: v(0), right: v(5) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 4, line: 5, code: "mid = (left + right) // 2", locals: [fn({ left: v(0), right: v(5), mid: v(2) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 5, line: 9, code: "left = mid + 1", locals: [fn({ left: v(3), right: v(5), mid: v(2) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 6, line: 5, code: "mid = (left + right) // 2", locals: [fn({ left: v(3), right: v(5), mid: v(4) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 7, line: 11, code: "right = mid - 1", locals: [fn({ left: v(3), right: v(3), mid: v(4) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 8, line: 5, code: "mid = (left + right) // 2", locals: [fn({ left: v(3), right: v(3), mid: v(3) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 9, line: 7, code: "return mid", locals: [fn({ left: v(3), right: v(3), mid: v(3) }), mod({ target: v(7) })], globals: { ...G, target: v(7) }, heap: [arrHeap()], stdout: "" },
  { step: 10, line: 14, code: "result = binary_search(arr, 7)", locals: [mod({ target: v(7), result: v(3) })], globals: { ...G, target: v(7), result: v(3) }, heap: [arrHeap()], stdout: "" },
  { step: 11, line: 15, code: "print(result)", locals: [mod({ target: v(7), result: v(3) })], globals: { ...G, target: v(7), result: v(3) }, heap: [arrHeap()], stdout: "3" },
];