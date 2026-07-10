import { memo, useMemo } from "react";
import TreeSVG from "./TreeSVG";

// Build tree structure from heap object value.
// Uses node.id from trace data for stable identity, falling back to path-based IDs.
function buildTree(node, path) {
  if (!node) return null;

  const id = node.id || path.join(".");
  const result = { id, name: String(node.value ?? node.val ?? "?") };

  const hasLeft = node.left !== null && node.left !== undefined;
  const hasRight = node.right !== null && node.right !== undefined;

  if (hasLeft || hasRight) {
    result.children = [];
    result.children.push(
      hasLeft
        ? buildTree(node.left, [...path, "left"])
        : { id: [...path, "left"].join("."), name: "·", _phantom: true }
    );
    result.children.push(
      hasRight
        ? buildTree(node.right, [...path, "right"])
        : { id: [...path, "right"].join("."), name: "·", _phantom: true }
    );
  }

  return result;
}

function TreeView({ object, events }) {
  const rootData = useMemo(
    () => buildTree(object.value, []),
    [object.value]
  );
  return <TreeSVG rootData={rootData} events={events} label={`${object.id} · tree`} />;
}

export default memo(TreeView);