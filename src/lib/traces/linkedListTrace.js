// Linked list trace — demonstrates node insertion, traversal, and head/current pointers.

export const LINKED_LIST_CODE = `class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
current = head
while current:
    print(current.val)
    current = current.next`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const mod = (extra = {}) => f("frame_mod", "<module>", extra);
const ll = (nodes) => h("ll", "linkedlist", nodes);

export const linkedListTrace = [
  // 0: head = Node(1)
  { step: 0, line: 6, code: "head = Node(1)", locals: [mod({ head: r("ll") })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }])], stdout: "" },

  // 1: head.next = Node(2)
  { step: 1, line: 7, code: "head.next = Node(2)", locals: [mod({ head: r("ll") })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }])], stdout: "" },

  // 2: head.next.next = Node(3)
  { step: 2, line: 8, code: "head.next.next = Node(3)", locals: [mod({ head: r("ll") })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "" },

  // 3: current = head
  { step: 3, line: 9, code: "current = head", locals: [mod({ head: r("ll"), current: v(0) })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "" },

  // 4: print(current.val) → 1
  { step: 4, line: 11, code: "print(current.val)", locals: [mod({ head: r("ll"), current: v(0) })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "1" },

  // 5: current = current.next
  { step: 5, line: 12, code: "current = current.next", locals: [mod({ head: r("ll"), current: v(1) })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "1" },

  // 6: print(current.val) → 2
  { step: 6, line: 11, code: "print(current.val)", locals: [mod({ head: r("ll"), current: v(1) })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "1\n2" },

  // 7: current = current.next
  { step: 7, line: 12, code: "current = current.next", locals: [mod({ head: r("ll"), current: v(2) })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "1\n2" },

  // 8: print(current.val) → 3
  { step: 8, line: 11, code: "print(current.val)", locals: [mod({ head: r("ll"), current: v(2) })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "1\n2\n3" },

  // 9: current = current.next → null (exit loop)
  { step: 9, line: 12, code: "current = current.next", locals: [mod({ head: r("ll") })], globals: { head: r("ll") }, heap: [ll([{ value: 1 }, { value: 2 }, { value: 3 }])], stdout: "1\n2\n3" },
];