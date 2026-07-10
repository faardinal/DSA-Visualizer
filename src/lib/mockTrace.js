// Top K Frequent Elements — mock execution trace
// Matches the Snapshot schema exactly: { step, line, code, locals, globals, heap, stdout }

export const SAMPLE_CODE = `def topKFrequent(nums, k):
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
    result = []
    for num in count:
        result.append(num)
    return result[:k]

nums = [1, 1, 2, 2, 2, 3]
k = 2
result = topKFrequent(nums, k)
print(result)`;

const NUMS = [1, 1, 2, 2, 2, 3];

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });

function snap(step, line, code, locals, globals, heap, stdout = "") {
  return { step, line, code, locals, globals, heap, stdout };
}

function frame(frame_id, func, vars) {
  return { frame_id, func, vars };
}

function heapObj(id, type, value) {
  return { id, type, value };
}

const numsHeap = () => heapObj("list_nums", "list", [...NUMS]);
const moduleFrame = (extra = {}) => frame("frame_module", "<module>", { nums: r("list_nums"), k: v(2), ...extra });
const funcFrame = (extra = {}) => frame("frame_func", "topKFrequent", { nums: r("list_nums"), k: v(2), ...extra });

export const mockTrace = [
  snap(0, 10, "nums = [1, 1, 2, 2, 2, 3]",
    [moduleFrame()],
    { nums: r("list_nums") },
    [numsHeap()]),

  snap(1, 11, "k = 2",
    [moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap()]),

  snap(2, 12, "result = topKFrequent(nums, k)",
    [funcFrame(), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap()]),

  snap(3, 2, "count = {}",
    [funcFrame({ count: r("dict_count") }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", {})]),

  snap(4, 3, "for num in nums:",
    [funcFrame({ count: r("dict_count"), num: v(1) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", {})]),

  snap(5, 4, "count[num] = count.get(num, 0) + 1",
    [funcFrame({ count: r("dict_count"), num: v(1) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 1 })]),

  snap(6, 3, "for num in nums:",
    [funcFrame({ count: r("dict_count"), num: v(1) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 1 })]),

  snap(7, 4, "count[num] = count.get(num, 0) + 1",
    [funcFrame({ count: r("dict_count"), num: v(1) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2 })]),

  snap(8, 3, "for num in nums:",
    [funcFrame({ count: r("dict_count"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2 })]),

  snap(9, 4, "count[num] = count.get(num, 0) + 1",
    [funcFrame({ count: r("dict_count"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 1 })]),

  snap(10, 3, "for num in nums:",
    [funcFrame({ count: r("dict_count"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 1 })]),

  snap(11, 4, "count[num] = count.get(num, 0) + 1",
    [funcFrame({ count: r("dict_count"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 2 })]),

  snap(12, 3, "for num in nums:",
    [funcFrame({ count: r("dict_count"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 2 })]),

  snap(13, 4, "count[num] = count.get(num, 0) + 1",
    [funcFrame({ count: r("dict_count"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3 })]),

  snap(14, 3, "for num in nums:",
    [funcFrame({ count: r("dict_count"), num: v(3) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3 })]),

  snap(15, 4, "count[num] = count.get(num, 0) + 1",
    [funcFrame({ count: r("dict_count"), num: v(3) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 })]),

  snap(16, 5, "result = []",
    [funcFrame({ count: r("dict_count"), result: r("list_result") }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [])]),

  snap(17, 6, "for num in count:",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(1) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [])]),

  snap(18, 7, "result.append(num)",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(1) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [1])]),

  snap(19, 6, "for num in count:",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [1])]),

  snap(20, 7, "result.append(num)",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(2) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [1, 2])]),

  snap(21, 6, "for num in count:",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(3) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [1, 2])]),

  snap(22, 7, "result.append(num)",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(3) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [1, 2, 3])]),

  snap(23, 8, "return result[:k]",
    [funcFrame({ count: r("dict_count"), result: r("list_result"), num: v(3) }), moduleFrame()],
    { nums: r("list_nums"), k: v(2) },
    [numsHeap(), heapObj("dict_count", "dict", { "1": 2, "2": 3, "3": 1 }), heapObj("list_result", "list", [1, 2, 3])]),

  snap(24, 12, "result = topKFrequent(nums, k)",
    [moduleFrame({ result: r("list_result") })],
    { nums: r("list_nums"), k: v(2), result: r("list_result") },
    [numsHeap(), heapObj("list_result", "list", [1, 2])]),

  snap(25, 13, "print(result)",
    [moduleFrame({ result: r("list_result") })],
    { nums: r("list_nums"), k: v(2), result: r("list_result") },
    [numsHeap(), heapObj("list_result", "list", [1, 2])],
    "[1, 2]"),
];