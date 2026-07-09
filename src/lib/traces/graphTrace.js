// Graph BFS trace — demonstrates BFS traversal with node highlighting.
// Graph stored as { nodes: [{id}], links: [{source, target}] }.
// Highlights field drives which nodes are "current" or "visited".

export const GRAPH_CODE = `from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': []
}

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

bfs(graph, 'A')`;

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

function fn(extra) {
  if (!extra) extra = {};
  return f("frame_bfs", "bfs", extra);
}

var graphValue = {
  nodes: [{ id: "A" }, { id: "B" }, { id: "C" }, { id: "D" }, { id: "E" }],
  links: [
    { source: "A", target: "B" },
    { source: "A", target: "C" },
    { source: "B", target: "D" },
    { source: "C", target: "D" },
    { source: "D", target: "E" },
  ],
};

function graphHeap() {
  return h("graph_g", "graph", graphValue);
}

function hl(nodeId, reason) {
  return { objectId: "graph_g", path: ["nodes", nodeId], metadata: { reason: reason } };
}

export const graphTrace = [
  {
    step: 0,
    line: 14,
    code: "bfs(graph, 'A')",
    locals: [mod({ graph: r("graph_g") })],
    globals: { graph: r("graph_g") },
    heap: [graphHeap()],
    stdout: "",
  },
  {
    step: 1,
    line: 9,
    code: "visited.add(start)",
    locals: [
      fn({ graph: r("graph_g"), start: v("A"), visited: v("{A}"), queue: r("queue_q") }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["A"])],
    highlights: [hl("A", "current")],
    stdout: "",
  },
  {
    step: 2,
    line: 11,
    code: "node = queue.popleft()",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A}"),
        queue: r("queue_q"),
        node: v("A"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", [])],
    highlights: [hl("A", "visited")],
    stdout: "",
  },
  {
    step: 3,
    line: 13,
    code: "visited.add(neighbor)",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B}"),
        queue: r("queue_q"),
        node: v("A"),
        neighbor: v("B"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["B"])],
    highlights: [hl("A", "visited"), hl("B", "current")],
    stdout: "",
  },
  {
    step: 4,
    line: 13,
    code: "visited.add(neighbor)",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C}"),
        queue: r("queue_q"),
        node: v("A"),
        neighbor: v("C"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["B", "C"])],
    highlights: [hl("A", "visited"), hl("B", "visited"), hl("C", "current")],
    stdout: "",
  },
  {
    step: 5,
    line: 11,
    code: "node = queue.popleft()",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C}"),
        queue: r("queue_q"),
        node: v("B"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["C"])],
    highlights: [hl("A", "visited"), hl("B", "visited"), hl("C", "visited")],
    stdout: "",
  },
  {
    step: 6,
    line: 13,
    code: "visited.add(neighbor)",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C,D}"),
        queue: r("queue_q"),
        node: v("B"),
        neighbor: v("D"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["C", "D"])],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "current"),
    ],
    stdout: "",
  },
  {
    step: 7,
    line: 11,
    code: "node = queue.popleft()",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C,D}"),
        queue: r("queue_q"),
        node: v("C"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["D"])],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "visited"),
    ],
    stdout: "",
  },
  {
    step: 8,
    line: 12,
    code: "if neighbor not in visited:",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C,D}"),
        queue: r("queue_q"),
        node: v("C"),
        neighbor: v("D"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["D"])],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "visited"),
    ],
    stdout: "",
  },
  {
    step: 9,
    line: 11,
    code: "node = queue.popleft()",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C,D}"),
        queue: r("queue_q"),
        node: v("D"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", [])],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "visited"),
    ],
    stdout: "",
  },
  {
    step: 10,
    line: 13,
    code: "visited.add(neighbor)",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C,D,E}"),
        queue: r("queue_q"),
        node: v("D"),
        neighbor: v("E"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", ["E"])],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "visited"),
      hl("E", "current"),
    ],
    stdout: "",
  },
  {
    step: 11,
    line: 11,
    code: "node = queue.popleft()",
    locals: [
      fn({
        graph: r("graph_g"),
        start: v("A"),
        visited: v("{A,B,C,D,E}"),
        queue: r("queue_q"),
        node: v("E"),
      }),
      mod({ graph: r("graph_g") }),
    ],
    globals: { graph: r("graph_g") },
    heap: [graphHeap(), h("queue_q", "queue", [])],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "visited"),
      hl("E", "visited"),
    ],
    stdout: "",
  },
  {
    step: 12,
    line: 14,
    code: "return visited",
    locals: [mod({ graph: r("graph_g") })],
    globals: { graph: r("graph_g") },
    heap: [graphHeap()],
    highlights: [
      hl("A", "visited"),
      hl("B", "visited"),
      hl("C", "visited"),
      hl("D", "visited"),
      hl("E", "visited"),
    ],
    stdout: "",
  },
];