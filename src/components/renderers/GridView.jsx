import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function GridView({ object, events }) {
  const grid = object.value || [];
  const rows = grid.length;
  const cols = grid[0]?.length || 0;

  // Active cells (current cell being filled)
  const currentCells = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Highlight" && Array.isArray(e.path) && e.path.length === 2) {
        if (e.metadata?.reason === "current") {
          set.add(`${e.path[0]},${e.path[1]}`);
        }
      }
    }
    return set;
  }, [events]);

  // Dependency cells (softly highlighted — previous cells that contributed)
  const dependencyCells = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Highlight" && Array.isArray(e.path) && e.path.length === 2) {
        if (e.metadata?.reason === "dependency" || e.metadata?.reason === "visited") {
          set.add(`${e.path[0]},${e.path[1]}`);
        }
      }
    }
    return set;
  }, [events]);

  // Updated cells (value just changed)
  const updatedCells = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Update" && Array.isArray(e.path) && e.path.length === 2) {
        set.add(`${e.path[0]},${e.path[1]}`);
      }
      if (e.type === "Insert" && Array.isArray(e.path) && e.path.length === 2) {
        set.add(`${e.path[0]},${e.path[1]}`);
      }
    }
    return set;
  }, [events]);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="text-[11px] font-mono text-muted-foreground">
        <span className="font-medium">{object.id}</span>
        <span className="opacity-50 mx-1">·</span>
        <span>grid · {rows}×{cols}</span>
      </div>
      <div className="flex flex-col gap-0.5">
        {grid.map((row, ri) => (
          <div key={ri} className="flex gap-0.5">
            <AnimatePresence initial={false}>
              {row.map((cell, ci) => {
                const key = `${ri},${ci}`;
                const isCurrent = currentCells.has(key);
                const isDependency = dependencyCells.has(key);
                const isUpdated = updatedCells.has(key);
                const isFilled = cell !== 0 && cell !== null && cell !== undefined && cell !== "";

                return (
                  <motion.div
                    key={key}
                    layout
                    initial={{ opacity: 0, scale: 0.7 }}
                    animate={{
                      opacity: 1,
                      scale: 1,
                      backgroundColor: isCurrent
                        ? "hsl(var(--primary))"
                        : isDependency
                        ? "hsl(var(--primary) / 0.2)"
                        : isUpdated
                        ? "hsl(var(--primary) / 0.15)"
                        : isFilled
                        ? "hsl(var(--muted))"
                        : "hsl(var(--muted) / 0.3)",
                      color: isCurrent
                        ? "hsl(var(--primary-foreground))"
                        : "hsl(var(--foreground))",
                    }}
                    exit={{ opacity: 0, scale: 0.7 }}
                    transition={{ type: "spring", stiffness: 300, damping: 22 }}
                    className="w-10 h-10 flex items-center justify-center rounded-md font-mono text-xs"
                  >
                    {isFilled ? String(cell) : ""}
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </div>
  );
}

export default memo(GridView);