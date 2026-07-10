// BST insert trace — demonstrates tree node insertion with stable node identity.
// Tree value uses node.id for stable identity across snapshots.

export const TREE_CODE = `class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

root = TreeNode(5)
root.left = TreeNode(3)
root.right = TreeNode(7)
root.left.left = TreeNode(1)
root.left.right = TreeNode(4)`;

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

function node(id, val, left, right) {
  if (left === undefined) left = null;
  if (right === undefined) right = null;
  return { id: id, value: val, left: left, right: right };
}

export const treeTrace = [
  {
    step: 0,
    line: 6,
    code: "root = TreeNode(5)",
    locals: [mod({ root: r("tree_root") })],
    globals: { root: r("tree_root") },
    heap: [h("tree_root", "tree", node("n5", 5))],
    stdout: "",
  },
  {
    step: 1,
    line: 7,
    code: "root.left = TreeNode(3)",
    locals: [mod({ root: r("tree_root") })],
    globals: { root: r("tree_root") },
    heap: [h("tree_root", "tree", node("n5", 5, node("n3", 3)))],
    stdout: "",
  },
  {
    step: 2,
    line: 8,
    code: "root.right = TreeNode(7)",
    locals: [mod({ root: r("tree_root") })],
    globals: { root: r("tree_root") },
    heap: [h("tree_root", "tree", node("n5", 5, node("n3", 3), node("n7", 7)))],
    stdout: "",
  },
  {
    step: 3,
    line: 9,
    code: "root.left.left = TreeNode(1)",
    locals: [mod({ root: r("tree_root") })],
    globals: { root: r("tree_root") },
    heap: [
      h("tree_root", "tree", node("n5", 5, node("n3", 3, node("n1", 1)), node("n7", 7))),
    ],
    stdout: "",
  },
  {
    step: 4,
    line: 10,
    code: "root.left.right = TreeNode(4)",
    locals: [mod({ root: r("tree_root") })],
    globals: { root: r("tree_root") },
    heap: [
      h(
        "tree_root",
        "tree",
        node("n5", 5, node("n3", 3, node("n1", 1), node("n4", 4)), node("n7", 7))
      ),
    ],
    stdout: "",
  },
];