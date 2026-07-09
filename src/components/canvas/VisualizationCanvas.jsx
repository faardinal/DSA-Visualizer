import { memo, useMemo } from "react";
import ArrayView from "@/components/renderers/ArrayView";
import HashMapView from "@/components/renderers/HashMapView";
import StackView from "@/components/renderers/StackView";
import QueueView from "@/components/renderers/QueueView";
import TreeView from "@/components/renderers/TreeView";
import HeapView from "@/components/renderers/HeapView";
import LinkedListView from "@/components/renderers/LinkedListView";
import GraphView from "@/components/renderers/GraphView";
import GridView from "@/components/renderers/GridView";
import SetView from "@/components/renderers/SetView";
import ObjectView from "@/components/renderers/ObjectView";
import { extractPointers } from "@/lib/pointerSystem";

// Heap entry types that carry no visualizable state at all — safe to always skip.
const SKIP_TYPES = new Set(["function", "unsupported", "module", "type"]);

const RENDERERS = {
  list: ArrayView,
  array: ArrayView,
  tuple: ArrayView,
  set: SetView,
  dict: HashMapView,
  hashmap: HashMapView,
  stack: StackView,
  queue: QueueView,
  tree: TreeView,
  bst: TreeView,
  heap: HeapView,
  linkedlist: LinkedListView,
  graph: GraphView,
  grid: GridView,
};

function VisualizationCanvas({ snapshot, events }) {
  // Extract pointers — ONLY recognized names, from top frame.
  // Pointers automatically disappear when the variable no longer exists.
  const pointers = useMemo(() => extractPointers(snapshot), [snapshot]);

  if (!snapshot) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground text-sm">
        No trace loaded. Click Run to visualize.
      </div>
    );
  }

  const heap = snapshot.heap || [];
  const visualizable = heap.filter((obj) => !SKIP_TYPES.has(obj.type));

  if (visualizable.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground text-sm">
        No visualizable data structures in this step.
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto p-8 flex flex-col items-center justify-center gap-12">
      {visualizable.map((obj) => {
        const Renderer = RENDERERS[obj.type] || ObjectView;
        const objEvents = events.filter((e) => e.objectId === obj.id);
        return (
          <Renderer
            key={obj.id}
            object={obj}
            events={objEvents}
            pointers={pointers}
          />
        );
      })}
    </div>
  );
}

export default memo(VisualizationCanvas);