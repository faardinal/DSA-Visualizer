import { memo, useEffect, useRef, useState, useMemo } from "react";
import { motion } from "framer-motion";
import { forceSimulation, forceManyBody, forceLink, forceCenter, forceX, forceY } from "d3-force";

const GRAPH_WIDTH = 420;
const GRAPH_HEIGHT = 320;

function GraphView({ object, events }) {
  const { nodes: rawNodes = [], links: rawLinks = [] } = object.value || {};

  // Ref to preserve positions across re-renders (stable layout)
  const positionsRef = useRef({});
  const [positions, setPositions] = useState({});

  // Active node IDs from events
  const activeNodeIds = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Highlight" || e.type === "Insert" || e.type === "Update") {
        if (Array.isArray(e.path) && e.path[0] === "nodes" && e.path[1]) {
          set.add(e.path[1]);
        }
      }
    }
    return set;
  }, [events]);

  // Active link indices from events
  const activeLinkIndices = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Highlight" && Array.isArray(e.path) && e.path[0] === "links" && e.path[1] !== undefined) {
        set.add(e.path[1]);
      }
    }
    return set;
  }, [events]);

  // Visited nodes (from metadata reason === "visit" or "visited")
  const visitedNodeIds = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Highlight" && Array.isArray(e.path) && e.path[0] === "nodes") {
        const reason = e.metadata?.reason;
        if (reason === "visit" || reason === "visited" || reason === "current") {
          set.add(e.path[1]);
        }
      }
    }
    return set;
  }, [events]);

  useEffect(() => {
    if (!rawNodes.length) return;

    // Preserve existing positions, initialize new nodes
    const prevPos = positionsRef.current;
    const simNodes = rawNodes.map((n) => ({
      ...n,
      x: prevPos[n.id]?.x ?? Math.random() * GRAPH_WIDTH,
      y: prevPos[n.id]?.y ?? Math.random() * GRAPH_HEIGHT,
    }));

    const simLinks = rawLinks.map((l) => ({
      source: typeof l.source === "object" ? l.source.id : l.source,
      target: typeof l.target === "object" ? l.target.id : l.target,
    }));

    const sim = forceSimulation(simNodes)
      .force("charge", forceManyBody().strength(-300))
      .force("link", forceLink(simLinks).id((d) => d.id).distance(90))
      .force("center", forceCenter(GRAPH_WIDTH / 2, GRAPH_HEIGHT / 2))
      .force("x", forceX(GRAPH_WIDTH / 2).strength(0.05))
      .force("y", forceY(GRAPH_HEIGHT / 2).strength(0.05))
      .alphaDecay(0.03);

    sim.on("tick", () => {
      const pos = {};
      simNodes.forEach((n) => {
        pos[n.id] = { x: n.x, y: n.y };
      });
      setPositions(pos);
    });

    return () => {
      // Store final positions before cleanup
      const pos = {};
      simNodes.forEach((n) => {
        pos[n.id] = { x: n.x, y: n.y };
      });
      positionsRef.current = pos;
      sim.stop();
    };
  }, [rawNodes, rawLinks]);

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="text-[11px] font-mono text-muted-foreground">
        <span className="font-medium">{object.id}</span>
        <span className="opacity-50 mx-1">·</span>
        <span>graph · {rawNodes.length} nodes · {rawLinks.length} edges</span>
      </div>
      <svg width={GRAPH_WIDTH} height={GRAPH_HEIGHT}>
        {/* Links */}
        {rawLinks.map((link, i) => {
          const sId = typeof link.source === "object" ? link.source.id : link.source;
          const tId = typeof link.target === "object" ? link.target.id : link.target;
          const s = positions[sId];
          const t = positions[tId];
          if (!s || !t) return null;
          const isActive = activeLinkIndices.has(i);
          return (
            <motion.line
              key={`link-${i}`}
              animate={{ x1: s.x, y1: s.y, x2: t.x, y2: t.y }}
              transition={{ type: "spring", stiffness: 200, damping: 20 }}
              stroke={isActive ? "hsl(var(--primary))" : "hsl(var(--border))"}
              strokeWidth={isActive ? 2.5 : 1.5}
            />
          );
        })}

        {/* Nodes */}
        {rawNodes.map((node) => {
          const pos = positions[node.id];
          if (!pos) return null;
          const isActive = activeNodeIds.has(node.id);
          const isVisited = visitedNodeIds.has(node.id);
          return (
            <motion.g
              key={node.id}
              animate={{ x: pos.x, y: pos.y }}
              transition={{ type: "spring", stiffness: 200, damping: 20 }}
            >
              <circle
                r={18}
                fill={
                  isActive
                    ? "hsl(var(--primary))"
                    : isVisited
                    ? "hsl(var(--primary) / 0.3)"
                    : "hsl(var(--muted))"
                }
                stroke={
                  isActive || isVisited
                    ? "hsl(var(--primary))"
                    : "hsl(var(--border))"
                }
                strokeWidth={isActive ? 2 : 1}
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
                {node.id}
              </text>
            </motion.g>
          );
        })}
      </svg>
    </div>
  );
}

export default memo(GraphView);