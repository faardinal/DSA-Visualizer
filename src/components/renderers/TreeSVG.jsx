import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { hierarchy, tree } from "d3-hierarchy";

// Shared tree SVG renderer — used by TreeView and HeapView.
// D3 computes layout coordinates ONLY. React renders the DOM.
// Framer Motion animates everything with transform-based transitions.
// Node identity is stable: uses node.data.id (from trace data or path-based).
function TreeSVG({ rootData, events, label }) {
  const { nodes, links, width, height } = useMemo(() => {
    if (!rootData) return { nodes: [], links: [], width: 200, height: 100 };
    const root = hierarchy(rootData);
    tree().nodeSize([48, 64])(root);
    const allNodes = root.descendants();
    const w = Math.max(...allNodes.map((n) => Math.abs(n.x)), 100) * 2 + 80;
    const h = Math.max(...allNodes.map((n) => n.y), 80) + 80;
    return { nodes: allNodes, links: root.links(), width: w, height: h };
  }, [rootData]);

  const offsetX = width / 2;
  const offsetY = 40;

  // Active node IDs from events
  const activeIds = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (["Highlight", "Pulse", "Swap", "Insert", "Update"].includes(e.type)) {
        // For tree events, path is an array — build node ID from path
        if (Array.isArray(e.path) && e.path.length > 0) {
          set.add(e.path.join("."));
          // Also add parent paths
          for (let i = 1; i <= e.path.length; i++) {
            set.add(e.path.slice(0, i).join("."));
          }
        }
      }
    }
    return set;
  }, [events]);

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="text-[11px] font-mono text-muted-foreground">{label}</div>
      <svg width={width} height={height} className="overflow-visible">
        {/* Links */}
        {links.map((link, i) => {
          if (link.target.data._phantom) return null;
          return (
            <motion.line
              key={`link-${i}`}
              initial={{ opacity: 0 }}
              animate={{
                opacity: 1,
                x1: link.source.x + offsetX,
                y1: link.source.y + offsetY,
                x2: link.target.x + offsetX,
                y2: link.target.y + offsetY,
              }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
              stroke="hsl(var(--border))"
              strokeWidth={1.5}
            />
          );
        })}

        {/* Nodes */}
        <AnimatePresence>
          {nodes.map((node) => {
            if (node.data._phantom) {
              return (
                <circle
                  key={node.data.id}
                  cx={node.x + offsetX}
                  cy={node.y + offsetY}
                  r={3}
                  fill="hsl(var(--border))"
                  opacity={0.3}
                />
              );
            }
            const isActive = activeIds.has(node.data.id);
            return (
              <motion.g
                key={node.data.id}
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{
                  opacity: 1,
                  scale: 1,
                  x: node.x + offsetX,
                  y: node.y + offsetY,
                }}
                exit={{ opacity: 0, scale: 0.5 }}
                transition={{ type: "spring", stiffness: 300, damping: 22 }}
              >
                <circle
                  r={16}
                  fill={isActive ? "hsl(var(--primary))" : "hsl(var(--muted))"}
                  stroke="hsl(var(--border))"
                  strokeWidth={1}
                />
                <text
                  textAnchor="middle"
                  dy={5}
                  className="font-mono pointer-events-none"
                  style={{
                    fontSize: 11,
                    fill: isActive
                      ? "hsl(var(--primary-foreground))"
                      : "hsl(var(--foreground))",
                  }}
                >
                  {node.data.name}
                </text>
              </motion.g>
            );
          })}
        </AnimatePresence>
      </svg>
    </div>
  );
}

export default memo(TreeSVG);