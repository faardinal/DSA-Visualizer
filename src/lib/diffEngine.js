// Pure JavaScript diff engine — compares two snapshots by object ID.
// Produces typed DiffEvents with a standardized shape:
//   { type, objectId, path, oldValue, newValue, metadata }
//
// No React state. No DOM access. No renderer logic.
// Stable object IDs only — never array indices for identity.

function deepEqual(a, b) {
  if (a === b) return true;
  if (a === null || b === null) return false;
  if (typeof a !== typeof b) return false;
  if (typeof a !== "object") return false;
  if (Array.isArray(a)) {
    if (!Array.isArray(b) || a.length !== b.length) return false;
    return a.every((v, i) => deepEqual(v, b[i]));
  }
  const ak = Object.keys(a);
  const bk = Object.keys(b);
  if (ak.length !== bk.length) return false;
  return ak.every((k) => deepEqual(a[k], b[k]));
}

function evt(type, objectId, path, oldValue, newValue, metadata = {}) {
  return { type, objectId, path, oldValue, newValue, metadata };
}

// ─── List / Array / Stack / Queue / Heap ───────────────────────────
function diffList(prevObj, nextObj) {
  const events = [];
  const prevVal = prevObj.value || [];
  const nextVal = nextObj.value || [];
  const minLen = Math.min(prevVal.length, nextVal.length);

  // Detect changed positions
  const changes = [];
  for (let i = 0; i < minLen; i++) {
    if (!deepEqual(prevVal[i], nextVal[i])) {
      changes.push({ index: i, prev: prevVal[i], next: nextVal[i] });
    }
  }

  // Detect swaps: two positions exchanged values
  const used = new Set();
  for (const c of changes) {
    if (used.has(c.index)) continue;
    const partner = changes.find(
      (c2) =>
        c2.index !== c.index &&
        !used.has(c2.index) &&
        deepEqual(c2.prev, c.next) &&
        deepEqual(c2.next, c.prev)
    );
    if (partner) {
      events.push(
        evt("Swap", prevObj.id, null, null, null, {
          i: c.index,
          j: partner.index,
          prevI: c.prev,
          prevJ: partner.prev,
          nextI: c.next,
          nextJ: partner.next,
        })
      );
      used.add(c.index);
      used.add(partner.index);
    }
  }

  // Detect moves: value shifted from one position to another (not a swap)
  for (const c of changes) {
    if (used.has(c.index)) continue;
    const movedTo = changes.find(
      (c2) => c2.index !== c.index && !used.has(c2.index) && deepEqual(c2.next, c.prev)
    );
    if (movedTo && !deepEqual(c.next, movedTo.prev)) {
      events.push(
        evt("Move", prevObj.id, movedTo.index, c.prev, c.prev, {
          from: c.index,
          to: movedTo.index,
        })
      );
      used.add(c.index);
      used.add(movedTo.index);
    }
  }

  // Remaining changes are Updates (overwrite)
  for (const c of changes) {
    if (!used.has(c.index)) {
      events.push(evt("Update", prevObj.id, c.index, c.prev, c.next));
    }
  }

  // Resize event for length changes
  if (nextVal.length !== prevVal.length) {
    events.push(
      evt("Resize", prevObj.id, null, prevVal.length, nextVal.length, {
        delta: nextVal.length - prevVal.length,
      })
    );
  }

  // Insert / Delete at boundaries
  if (nextVal.length > prevVal.length) {
    for (let i = prevVal.length; i < nextVal.length; i++) {
      events.push(evt("Insert", prevObj.id, i, null, nextVal[i]));
    }
  } else if (prevVal.length > nextVal.length) {
    for (let i = nextVal.length; i < prevVal.length; i++) {
      events.push(evt("Delete", prevObj.id, i, prevVal[i], null));
    }
  }

  return events;
}

// ─── Dict / HashMap ───────────────────────────────────────────────
function diffDict(prevObj, nextObj) {
  const events = [];
  const prevVal = prevObj.value || {};
  const nextVal = nextObj.value || {};
  const prevKeys = Object.keys(prevVal);
  const nextKeys = Object.keys(nextVal);

  for (const key of nextKeys) {
    if (!(key in prevVal)) {
      events.push(evt("Insert", prevObj.id, key, null, nextVal[key]));
    } else if (!deepEqual(prevVal[key], nextVal[key])) {
      events.push(evt("Pulse", prevObj.id, key, prevVal[key], nextVal[key]));
    }
  }

  for (const key of prevKeys) {
    if (!(key in nextVal)) {
      events.push(evt("Delete", prevObj.id, key, prevVal[key], null));
    }
  }

  return events;
}

// ─── Tree / BST (nested object diff) ──────────────────────────────
function diffTree(prevNode, nextNode, objectId, path) {
  const events = [];

  if (!prevNode && !nextNode) return events;

  if (!prevNode && nextNode) {
    events.push(evt("Insert", objectId, path, null, nextNode));
    return events;
  }

  if (prevNode && !nextNode) {
    events.push(evt("Delete", objectId, path, prevNode, null));
    return events;
  }

  // Both exist — compare value
  const pv = prevNode.value ?? prevNode.val;
  const nv = nextNode.value ?? nextNode.val;
  if (!deepEqual(pv, nv)) {
    events.push(evt("Update", objectId, [...path, "value"], pv, nv));
  }

  // Recurse into children
  for (const childKey of ["left", "right"]) {
    events.push(...diffTree(prevNode[childKey], nextNode[childKey], objectId, [...path, childKey]));
  }

  return events;
}

// ─── Graph (nodes + links) ────────────────────────────────────────
function diffGraph(prevObj, nextObj) {
  const events = [];
  const prevVal = prevObj.value || {};
  const nextVal = nextObj.value || {};
  const prevNodes = prevVal.nodes || [];
  const nextNodes = nextVal.nodes || [];
  const prevLinks = prevVal.links || [];
  const nextLinks = nextVal.links || [];

  const prevNodeMap = new Map(prevNodes.map((n) => [n.id, n]));
  const nextNodeMap = new Map(nextNodes.map((n) => [n.id, n]));

  for (const [id, node] of nextNodeMap) {
    if (!prevNodeMap.has(id)) {
      events.push(evt("Insert", prevObj.id, ["nodes", id], null, node));
    } else if (!deepEqual(prevNodeMap.get(id), node)) {
      events.push(evt("Update", prevObj.id, ["nodes", id], prevNodeMap.get(id), node));
    }
  }

  for (const [id] of prevNodeMap) {
    if (!nextNodeMap.has(id)) {
      events.push(evt("Delete", prevObj.id, ["nodes", id], prevNodeMap.get(id), null));
    }
  }

  // Links — compare by index
  const maxLinks = Math.max(prevLinks.length, nextLinks.length);
  for (let i = 0; i < maxLinks; i++) {
    if (i >= prevLinks.length) {
      events.push(evt("Insert", prevObj.id, ["links", i], null, nextLinks[i]));
    } else if (i >= nextLinks.length) {
      events.push(evt("Delete", prevObj.id, ["links", i], prevLinks[i], null));
    } else if (!deepEqual(prevLinks[i], nextLinks[i])) {
      events.push(evt("Update", prevObj.id, ["links", i], prevLinks[i], nextLinks[i]));
    }
  }

  return events;
}

// ─── Grid (2D array) ──────────────────────────────────────────────
function diffGrid(prevObj, nextObj) {
  const events = [];
  const prevGrid = prevObj.value || [];
  const nextGrid = nextObj.value || [];
  const rows = Math.max(prevGrid.length, nextGrid.length);

  for (let r = 0; r < rows; r++) {
    const prevRow = prevGrid[r] || [];
    const nextRow = nextGrid[r] || [];
    const cols = Math.max(prevRow.length, nextRow.length);

    for (let c = 0; c < cols; c++) {
      if (c >= prevRow.length) {
        events.push(evt("Insert", prevObj.id, [r, c], null, nextRow[c]));
      } else if (c >= nextRow.length) {
        events.push(evt("Delete", prevObj.id, [r, c], prevRow[c], null));
      } else if (!deepEqual(prevRow[c], nextRow[c])) {
        events.push(evt("Update", prevObj.id, [r, c], prevRow[c], nextRow[c]));
      }
    }
  }

  return events;
}

// ─── Object dispatcher ────────────────────────────────────────────
function diffObject(prevObj, nextObj) {
  const events = [];
  if (prevObj.type !== nextObj.type) return events;

  const type = nextObj.type;

  if (["list", "tuple", "array", "stack", "queue", "set", "heap"].includes(type)) {
    events.push(...diffList(prevObj, nextObj));
  } else if (type === "dict" || type === "hashmap") {
    events.push(...diffDict(prevObj, nextObj));
  } else if (type === "tree" || type === "bst") {
    events.push(...diffTree(prevObj.value, nextObj.value, prevObj.id, []));
  } else if (type === "linkedlist") {
    events.push(...diffList(prevObj, nextObj));
  } else if (type === "graph") {
    events.push(...diffGraph(prevObj, nextObj));
  } else if (type === "grid") {
    events.push(...diffGrid(prevObj, nextObj));
  } else if (!deepEqual(prevObj.value, nextObj.value)) {
    events.push(evt("Update", nextObj.id, null, prevObj.value, nextObj.value));
  }

  return events;
}

// ─── Main entry point ─────────────────────────────────────────────
export function diffSnapshots(prev, next) {
  if (!prev || !next) return [];
  const events = [];

  const prevHeap = new Map((prev.heap || []).map((o) => [o.id, o]));
  const nextHeap = new Map((next.heap || []).map((o) => [o.id, o]));

  // Deleted objects
  for (const [id, obj] of prevHeap) {
    if (!nextHeap.has(id)) {
      events.push(evt("Delete", id, null, obj, null));
    }
  }

  // Inserted or modified objects
  for (const [id, obj] of nextHeap) {
    const prevObj = prevHeap.get(id);
    if (!prevObj) {
      events.push(evt("Insert", id, null, null, obj, { objectType: obj.type }));
    } else {
      events.push(...diffObject(prevObj, obj));
    }
  }

  // Pass through explicit highlights from the snapshot
  if (next.highlights) {
    for (const h of next.highlights) {
      events.push(
        evt("Highlight", h.objectId, h.path ?? null, null, null, h.metadata || {})
      );
    }
  }

  return events;
}

// ─── Variable diff (for Variables panel) ───────────────────────────
export function diffVariables(prevSnapshot, nextSnapshot) {
  if (!prevSnapshot || !nextSnapshot) return {};

  const result = {};
  const prevFrame = prevSnapshot.locals?.[0];
  const nextFrame = nextSnapshot.locals?.[0];
  const prevVars = prevFrame?.vars || {};
  const nextVars = nextFrame?.vars || {};

  const allNames = new Set([...Object.keys(prevVars), ...Object.keys(nextVars)]);

  for (const name of allNames) {
    const prevVal = prevVars[name];
    const nextVal = nextVars[name];

    if (!prevVal && nextVal) {
      result[name] = { oldValue: null, newValue: nextVal, change: "added" };
    } else if (prevVal && !nextVal) {
      result[name] = { oldValue: prevVal, newValue: null, change: "removed" };
    } else if (!deepEqual(prevVal, nextVal)) {
      result[name] = { oldValue: prevVal, newValue: nextVal, change: "changed" };
    }
  }

  return result;
}