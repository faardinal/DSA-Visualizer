// Queue trace — demonstrates enqueue (slide in from right) and dequeue (slide out left).

export const QUEUE_CODE = `from collections import deque
queue = deque()
queue.append(10)
queue.append(20)
queue.append(30)
val = queue.popleft()
print(val)`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const mod = (extra = {}) => f("frame_mod", "<module>", extra);

export const queueTrace = [
  { step: 0, line: 2, code: "queue = deque()", locals: [mod({ queue: r("queue_q") })], globals: { queue: r("queue_q") }, heap: [h("queue_q", "queue", [])], stdout: "" },
  { step: 1, line: 3, code: "queue.append(10)", locals: [mod({ queue: r("queue_q") })], globals: { queue: r("queue_q") }, heap: [h("queue_q", "queue", [10])], stdout: "" },
  { step: 2, line: 4, code: "queue.append(20)", locals: [mod({ queue: r("queue_q") })], globals: { queue: r("queue_q") }, heap: [h("queue_q", "queue", [10, 20])], stdout: "" },
  { step: 3, line: 5, code: "queue.append(30)", locals: [mod({ queue: r("queue_q") })], globals: { queue: r("queue_q") }, heap: [h("queue_q", "queue", [10, 20, 30])], stdout: "" },
  { step: 4, line: 6, code: "val = queue.popleft()", locals: [mod({ queue: r("queue_q"), val: v(10) })], globals: { queue: r("queue_q"), val: v(10) }, heap: [h("queue_q", "queue", [20, 30])], stdout: "" },
  { step: 5, line: 7, code: "print(val)", locals: [mod({ queue: r("queue_q"), val: v(10) })], globals: { queue: r("queue_q"), val: v(10) }, heap: [h("queue_q", "queue", [20, 30])], stdout: "10" },
];