// Generates human-readable explanations for each step based on diff events.
// Uses the standardized event shape: { type, objectId, path, oldValue, newValue, metadata }.

function formatVal(val) {
  if (val === null || val === undefined) return "null";
  if (typeof val === "object") return JSON.stringify(val);
  return String(val);
}

function formatReturnValue(rv) {
  if (!rv) return "";
  if ("ref" in rv) return `{${rv.ref}}`;
  return formatVal(rv.value);
}

export function generateExplanation(snapshot, prevSnapshot, events) {
  if (!snapshot) return "Ready to visualize. Click Run to begin.";

  // Exceptions always take priority — this is the most important thing
  // happening in the snapshot.
  if (snapshot.event === "exception" && snapshot.exception) {
    return `${snapshot.exception.type}: ${snapshot.exception.message} (line ${snapshot.exception.line ?? snapshot.line}).`;
  }

  if (snapshot.event === "return") {
    const fn = snapshot.function;
    if (snapshot.returnValue !== undefined) {
      return `Returned ${formatReturnValue(snapshot.returnValue)} from ${fn}().`;
    }
    return `Returned from ${fn}() (no value).`;
  }

  if (!prevSnapshot)
    return `Starting execution at line ${snapshot.line}: ${snapshot.code?.trim()}`;

  // A newly-pushed frame relative to the previous snapshot means a function
  // was just called (the backend has no explicit 'call' event, so this is
  // inferred from the reconstructed call stack depth).
  const prevDepth = prevSnapshot.locals?.length ?? 1;
  const currDepth = snapshot.locals?.length ?? 1;
  if (snapshot.event === "line" && currDepth > prevDepth) {
    return `Called ${snapshot.function}(): ${snapshot.code?.trim()}`;
  }

  const code = snapshot.code?.trim() || "";
  const inserts = events.filter((e) => e.type === "Insert");
  const deletes = events.filter((e) => e.type === "Delete");
  const pulses = events.filter((e) => e.type === "Pulse");
  const swaps = events.filter((e) => e.type === "Swap");
  const updates = events.filter((e) => e.type === "Update");
  const moves = events.filter((e) => e.type === "Move");
  const resizes = events.filter((e) => e.type === "Resize");
  const highlights = events.filter((e) => e.type === "Highlight");

  if (swaps.length > 0) {
    const s = swaps[0];
    return `Swapped elements at indices ${s.metadata?.i} and ${s.metadata?.j}.`;
  }

  if (moves.length > 0) {
    const m = moves[0];
    return `Moved element from index ${m.metadata?.from} to ${m.metadata?.to}.`;
  }

  if (inserts.length > 0 && pulses.length === 0) {
    const ins = inserts[0];
    if (typeof ins.path === "string") {
      return `Inserted key "${ins.path}" with value ${formatVal(ins.newValue)}.`;
    }
    if (typeof ins.path === "number") {
      return `Inserted ${formatVal(ins.newValue)} at index ${ins.path}.`;
    }
    if (Array.isArray(ins.path)) {
      return `Created new node at ${ins.path.join(" → ")}.`;
    }
    return `Created new ${ins.metadata?.objectType || "object"}.`;
  }

  if (pulses.length > 0) {
    const p = pulses[0];
    if (typeof p.path === "string") {
      return `Updated key "${p.path}" from ${formatVal(p.oldValue)} to ${formatVal(p.newValue)}.`;
    }
    return `Updated a value.`;
  }

  if (updates.length > 0) {
    const u = updates[0];
    if (typeof u.path === "number") {
      return `Changed index ${u.path} from ${formatVal(u.oldValue)} to ${formatVal(u.newValue)}.`;
    }
    if (Array.isArray(u.path)) {
      return `Updated value at ${u.path.join(" → ")}.`;
    }
    return `Updated a value.`;
  }

  if (deletes.length > 0) {
    const d = deletes[0];
    if (typeof d.path === "string") {
      return `Removed key "${d.path}".`;
    }
    if (typeof d.path === "number") {
      return `Removed element at index ${d.path}.`;
    }
    if (Array.isArray(d.path)) {
      return `Removed node at ${d.path.join(" → ")}.`;
    }
    return `Removed an object.`;
  }

  if (resizes.length > 0) {
    const r = resizes[0];
    const delta = r.metadata?.delta;
    if (delta > 0) {
      return `Grew from ${r.oldValue} to ${r.newValue} elements.`;
    }
    return `Shrunk from ${r.oldValue} to ${r.newValue} elements.`;
  }

  if (highlights.length > 0) {
    const h = highlights[0];
    const reason = h.metadata?.reason;
    if (reason === "current" && Array.isArray(h.path)) {
      return `Visiting cell [${h.path.join(", ")}].`;
    }
    if (reason === "visit" || reason === "visited") {
      return `Visiting node ${Array.isArray(h.path) ? h.path[h.path.length - 1] : h.path}.`;
    }
  }

  if (snapshot.stdout && (!prevSnapshot.stdout || snapshot.stdout !== prevSnapshot.stdout)) {
    return `Printed output: ${snapshot.stdout.trim()}`;
  }

  return `Executing: ${code}`;
}