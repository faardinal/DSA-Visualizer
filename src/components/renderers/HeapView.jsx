import { memo, useMemo } from "react";
import TreeSVG from "./TreeSVG";

// Build heap tree from array representation.
// Node identity is path-based: "heap-0", "heap-1", etc. (index in array).
// This keeps identity stable when values swap during heapify.
function buildHeapTree(arr, index, path) {
  if (index >= arr.length) return null;

  const id = path.join(".");
  const result = { id, name: String(arr[index]) };

  const leftIdx = 2 * index + 1;
  const rightIdx = 2 * index + 2;
  const hasLeft = leftIdx < arr.length;
  const hasRight = rightIdx < arr.length;

  if (hasLeft || hasRight) {
    result.children = [];
    result.children.push(
      hasLeft
        ? buildHeapTree(arr, leftIdx, [...path, "left"])
        : { id: [...path, "left"].join("."), name: "·", _phantom: true }
    );
    result.children.push(
      hasRight
        ? buildHeapTree(arr, rightIdx, [...path, "right"])
        : { id: [...path, "right"].join("."), name: "·", _phantom: true }
    );
  }

  return result;
}

function HeapView({ object, events }) {
  const rootData = useMemo(
    () => buildHeapTree(object.value || [], 0, ["heap"]),
    [object.value]
  );

  // Swap events highlight specific indices
  const heapEvents = useMemo(() => {
    return events.map((e) => {
      if (e.type === "Swap" && e.metadata) {
        // Convert array indices to tree paths
        const pathI = indexToPath(e.metadata.i);
        const pathJ = indexToPath(e.metadata.j);
        return {
          ...e,
          path: pathI,
          metadata: { ...e.metadata, pathI, pathJ },
        };
      }
      return e;
    });
  }, [events]);

  return <TreeSVG rootData={rootData} events={heapEvents} label={`${object.id} · heap`} />;
}

// Convert heap array index to tree path: 0→[], 1→["left"], 2→["right"], etc.
function indexToPath(index) {
  if (index === 0) return [];
  const path = [];
  let i = index;
  while (i > 0) {
    const parent = Math.floor((i - 1) / 2);
    path.unshift(i === 2 * parent + 1 ? "left" : "right");
    i = parent;
  }
  return path;
}

export default memo(HeapView);