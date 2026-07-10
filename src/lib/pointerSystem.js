// Recognized pointer variable names.
// Only these variable names are treated as array/list pointers.
// All other integer locals are displayed as regular variables — never as pointers.
export const POINTER_NAMES = new Set([
  "left", "right", "mid", "low", "high", "pivot",
  "i", "j", "k", "front", "rear", "top",
  "head", "tail", "current", "parent", "child",
]);

// Extract pointers from a snapshot's top frame variables.
// Returns [{ name, index }] for recognized pointer names with integer values.
// Pointers automatically disappear when the variable no longer exists.
export function extractPointers(snapshot) {
  if (!snapshot?.locals?.[0]?.vars) return [];
  const vars = snapshot.locals[0].vars;
  return Object.entries(vars)
    .filter(
      ([name, v]) =>
        POINTER_NAMES.has(name) &&
        "value" in v &&
        typeof v.value === "number" &&
        Number.isInteger(v.value)
    )
    .map(([name, v]) => ({ name, index: v.value }));
}

// Extract a selected range from pointer pairs (e.g., left..right for binary search).
// Returns { start, end } if a range-defining pair of pointers exists, else null.
export function extractRange(pointers) {
  const pairs = [
    ["left", "right"],
    ["low", "high"],
  ];
  for (const [lo, hi] of pairs) {
    const p1 = pointers.find((p) => p.name === lo);
    const p2 = pointers.find((p) => p.name === hi);
    if (p1 && p2) {
      return {
        start: Math.min(p1.index, p2.index),
        end: Math.max(p1.index, p2.index),
      };
    }
  }
  return null;
}