// Adapts the real Flask backend's trace contract into the frontend's internal
// trace schema (the same shape the hand-authored files in src/lib/traces/* and
// mockTrace.js use), so every consumer — Timeline, VariablesPanel,
// CallStackPanel, VisualizationCanvas, diffEngine — can stay backend-agnostic.
//
// Backend shape (backend/routes.py::snapshot_to_dict), per snapshot:
//   { step, event, line, function, code, locals, globals, stdout, heap,
//     frame_id, call_stack: [{frame_id, function}], exception? }
//   - locals / globals: flat `{ name: primitive | {ref: heapId} }` for the
//     SINGLE currently-active frame only.
//   - frame_id / call_stack: unique per-call identity (Phase 3), so recursive
//     calls of the same function can be told apart. Older backend responses
//     (or hand-authored fixtures) may omit these — we fall back to the
//     previous function-name heuristic in that case.
//   - heap: dict keyed by heap-id string ->
//       { type: 'list'|'tuple'|'set', elements: [...] }
//       { type: 'dict', entries: [[key, value], ...] }
//       { type: <ClassName>, attributes: {...} }   (custom objects)
//       { type: 'unsupported', reason?, class_name? }  (things that can't be
//         visualized — generators, iterators, objects that failed to
//         serialize, or the heap-size cap being hit)
//
// Frontend internal shape (see mockTrace.js), per snapshot:
//   { step, line, code, stdout, locals: [{frame_id, func, vars}], globals, heap: [{id, type, value}] }
//   - vars: `{ name: {value} | {ref} }`
//   - heap: array of `{id, type, value}` where value is a raw array (list/tuple/set),
//     a raw object (dict), or raw attributes (custom types).
//
// Known, deliberate limitations:
//  - Graph-shaped custom objects (adjacency lists/dicts, arbitrary edge
//    representations) are too varied to reliably auto-detect without risking
//    false positives, so they fall back to the generic ObjectView/HashMapView
//    renderers rather than the dedicated GraphView. This is a graceful
//    fallback, not a crash — satisfies the Phase 3 "Execution Trace Only"
//    requirement for structures we can't confidently animate.

function wrapVar(raw) {
  if (raw !== null && typeof raw === "object" && "ref" in raw) return raw;
  return { value: raw };
}

function adaptVars(dict) {
  const out = {};
  for (const [name, raw] of Object.entries(dict || {})) {
    out[name] = wrapVar(raw);
  }
  return out;
}

function adaptHeapEntry(id, entry) {
  if (entry.type === "list" || entry.type === "tuple" || entry.type === "set") {
    return { id, type: entry.type, value: entry.elements || [] };
  }
  if (entry.type === "dict") {
    const value = {};
    for (const [key, val] of entry.entries || []) {
      const k = key !== null && typeof key === "object" ? JSON.stringify(key) : String(key);
      value[k] = val;
    }
    return { id, type: "dict", value };
  }
  // Custom class instance or unrecognized/unsupported type. Kept in the
  // array (rather than dropped) so ObjectView can render a generic fallback
  // and nothing silently disappears.
  return { id, type: entry.type, value: entry.attributes ?? null, className: entry.class_name };
}

function adaptHeap(rawHeap) {
  const out = [];
  for (const [id, entry] of Object.entries(rawHeap || {})) {
    out.push(adaptHeapEntry(id, entry));
  }
  return out;
}

// ─── Semantic structure detection ──────────────────────────────────────
// The backend only reports generic Python shapes (list/tuple/dict/set/
// <ClassName>). To light up the existing TreeView / LinkedListView
// renderers for real programs, we detect two common node-per-object
// patterns among custom-class heap entries and re-materialize them as a
// single synthetic heap object in the renderer's expected shape. Anything
// that doesn't match cleanly is left as a plain custom-class object, which
// ObjectView already renders — so nothing crashes or disappears.

function resolveRef(val, byId) {
  if (val !== null && typeof val === "object" && "ref" in val) {
    return byId.get(String(val.ref));
  }
  return undefined;
}

function isPlainValue(val) {
  return val === null || val === undefined || typeof val !== "object" || !("ref" in val);
}

// Detects a binary-tree-shaped node: has `left`/`right` attributes whose
// values are either null or refs to other objects of the same class shape.
function looksLikeTreeNode(entry) {
  if (!entry || entry.type !== "custom") return false;
  const attrs = entry.raw.attributes || {};
  return "left" in attrs && "right" in attrs;
}

// Detects a singly-linked-list node: has a `next` attribute, but not
// `left`/`right` (so trees aren't misclassified as lists).
function looksLikeListNode(entry) {
  if (!entry || entry.type !== "custom") return false;
  const attrs = entry.raw.attributes || {};
  return "next" in attrs && !("left" in attrs) && !("right" in attrs);
}

function pickNodeValue(attrs) {
  for (const key of ["value", "val", "data"]) {
    if (key in attrs && isPlainValue(attrs[key])) return attrs[key];
  }
  // Fall back to the first primitive attribute found.
  for (const [k, v] of Object.entries(attrs)) {
    if (k !== "next" && k !== "left" && k !== "right" && isPlainValue(v)) return v;
  }
  return null;
}

function buildTreeValue(id, byId, visited, depth = 0) {
  if (id == null || visited.has(id) || depth > 64) return null;
  const entry = byId.get(String(id));
  if (!entry || entry.type !== "custom") return null;
  visited.add(id);
  const attrs = entry.raw.attributes || {};
  const node = { id: entry.id, value: pickNodeValue(attrs) };

  const leftRef = attrs.left;
  const rightRef = attrs.right;
  node.left = leftRef && typeof leftRef === "object" && "ref" in leftRef
    ? buildTreeValue(leftRef.ref, byId, visited, depth + 1)
    : null;
  node.right = rightRef && typeof rightRef === "object" && "ref" in rightRef
    ? buildTreeValue(rightRef.ref, byId, visited, depth + 1)
    : null;
  return node;
}

function buildListChain(startId, byId) {
  const chain = [];
  const visited = new Set();
  let currentId = startId;
  while (currentId != null && !visited.has(currentId) && chain.length < 5000) {
    visited.add(currentId);
    const entry = byId.get(String(currentId));
    if (!entry || entry.type !== "custom") break;
    const attrs = entry.raw.attributes || {};
    chain.push({ id: entry.id, value: pickNodeValue(attrs) });
    const nextRef = attrs.next;
    currentId = nextRef && typeof nextRef === "object" && "ref" in nextRef ? nextRef.ref : null;
  }
  return { chain, ids: visited };
}

/**
 * Re-classifies node-per-object custom classes (linked lists, binary trees)
 * into the synthetic single-object shape the existing LinkedListView /
 * TreeView renderers expect, and drops the now-redundant per-node entries
 * from the top-level heap list so they don't render twice.
 */
function applySemanticDetection(heapArray, rawHeap) {
  const byId = new Map();
  for (const [id, entry] of Object.entries(rawHeap || {})) {
    const isCustom = !["list", "tuple", "set", "dict", "unsupported"].includes(entry.type);
    byId.set(id, { id, type: isCustom ? "custom" : entry.type, raw: entry });
  }

  const absorbedIds = new Set();
  const synthetic = [];

  // Tree roots: a tree-node that is not itself referenced as another node's
  // left/right child (so we build from the top, not from an interior node).
  const referencedAsChild = new Set();
  for (const entry of byId.values()) {
    if (!looksLikeTreeNode(entry)) continue;
    const attrs = entry.raw.attributes || {};
    for (const key of ["left", "right"]) {
      const ref = attrs[key];
      if (ref && typeof ref === "object" && "ref" in ref) referencedAsChild.add(String(ref.ref));
    }
  }
  for (const entry of byId.values()) {
    if (!looksLikeTreeNode(entry)) continue;
    if (referencedAsChild.has(entry.id) || absorbedIds.has(entry.id)) continue;
    const visited = new Set();
    const value = buildTreeValue(entry.id, byId, visited);
    if (!value || visited.size < 1) continue;
    for (const vid of visited) absorbedIds.add(String(vid));
    synthetic.push({ id: entry.id, type: "tree", value });
  }

  // Linked-list heads: a list-node not referenced as anyone else's `next`.
  const referencedAsNext = new Set();
  for (const entry of byId.values()) {
    if (!looksLikeListNode(entry)) continue;
    const attrs = entry.raw.attributes || {};
    const ref = attrs.next;
    if (ref && typeof ref === "object" && "ref" in ref) referencedAsNext.add(String(ref.ref));
  }
  for (const entry of byId.values()) {
    if (!looksLikeListNode(entry)) continue;
    if (referencedAsNext.has(entry.id) || absorbedIds.has(entry.id)) continue;
    const { chain, ids } = buildListChain(entry.id, byId);
    if (chain.length < 1) continue;
    for (const vid of ids) absorbedIds.add(String(vid));
    synthetic.push({ id: entry.id, type: "linkedlist", value: chain });
  }

  if (synthetic.length === 0) return heapArray;

  const filtered = heapArray.filter((obj) => !absorbedIds.has(String(obj.id)));
  return [...filtered, ...synthetic];
}

/**
 * Converts a raw backend trace (array of snapshots from POST /api/run) into
 * the frontend's internal trace format.
 *
 * @param {Array<object>} rawTrace
 * @returns {Array<object>} adapted trace, ready for Timeline/VariablesPanel/
 *   CallStackPanel/VisualizationCanvas/diffEngine.
 */
export function adaptBackendTrace(rawTrace) {
  if (!Array.isArray(rawTrace)) return [];

  const hasFrameIds = rawTrace.some((raw) => Array.isArray(raw.call_stack) && raw.call_stack.length > 0);

  // Reconstructed call stack, innermost-first (matches mockTrace convention:
  // `[funcFrame(), moduleFrame()]`). Each entry: { frame_id, func, vars }.
  const stack = [];
  let frameCounter = 0;
  // Module-level globals persist across the whole program even while paused
  // inside a nested call, but the backend only reports `globals` when the
  // active frame IS `<module>`. Carry the last known value forward so the
  // Globals panel doesn't go blank the moment you step into a function.
  let lastGlobals = {};

  return rawTrace.map((raw) => {
    const func = raw.function ?? "<module>";

    if (hasFrameIds) {
      // Precise reconstruction: the backend tells us exactly which frames
      // are on the stack right now (by unique frame_id), so recursive calls
      // of the same function are never confused with each other.
      const backendStack = raw.call_stack && raw.call_stack.length > 0
        ? raw.call_stack
        : [{ frame_id: 0, function: "<module>" }];
      const currentIds = new Set(backendStack.map((f) => `frame_${f.frame_id}`));

      // Drop any tracked frames that are no longer on the backend's stack.
      for (let i = stack.length - 1; i >= 0; i--) {
        if (!currentIds.has(stack[i].frame_id)) stack.splice(i, 1);
      }
      // Ensure every backend frame has a corresponding tracked entry, in
      // innermost-first order.
      const newStack = [];
      for (let i = backendStack.length - 1; i >= 0; i--) {
        const fid = `frame_${backendStack[i].frame_id}`;
        const existing = stack.find((f) => f.frame_id === fid);
        newStack.push(existing || { frame_id: fid, func: backendStack[i].function, vars: {} });
      }
      stack.length = 0;
      stack.push(...newStack);
    } else {
      // Legacy heuristic (no frame ids present — old fixtures/backend).
      const idx = stack.findIndex((f) => f.func === func);
      if (idx === -1) {
        stack.unshift({ frame_id: `frame_${frameCounter++}`, func, vars: {} });
      } else if (idx > 0) {
        stack.splice(0, idx);
      }
    }

    // The currently active frame always gets fresh, live vars from the backend.
    if (stack.length > 0) stack[0].vars = adaptVars(raw.locals);

    const localsSnapshot = stack.map((f) => ({ ...f }));

    if (func === "<module>") {
      lastGlobals = adaptVars(raw.globals);
    }

    const heap = applySemanticDetection(adaptHeap(raw.heap), raw.heap);

    const adapted = {
      step: raw.step,
      line: raw.line,
      code: raw.code,
      function: func,
      event: raw.event,
      stdout: raw.stdout ?? "",
      exception: raw.exception,
      locals: localsSnapshot,
      globals: lastGlobals,
      heap,
      // Only present on 'return' events (backend sets has_return_value).
      returnValue: raw.return_value !== undefined && raw.event === "return"
        ? wrapVar(raw.return_value)
        : undefined,
    };

    if (!hasFrameIds && raw.event === "return" && stack.length > 1) {
      // This frame is exiting after this snapshot — pop it so the *next*
      // snapshot's stack reflects the caller (legacy heuristic path only;
      // the frame_id path already tracks this precisely via call_stack).
      stack.shift();
    }

    return adapted;
  });
}
