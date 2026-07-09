import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function SetView({ object, events }) {
  const values = object.value || [];

  const activeIndices = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (typeof e.path === "number") {
        if (["Insert", "Highlight", "Pulse"].includes(e.type)) {
          set.add(e.path);
        }
      }
    }
    return set;
  }, [events]);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
        <span className="font-medium">{object.id}</span>
        <span className="opacity-50">·</span>
        <span>set · {values.length} items</span>
      </div>
      <div className="flex flex-wrap gap-2 justify-center max-w-[400px]">
        <AnimatePresence mode="popLayout" initial={false}>
          {values.map((val, i) => (
            <motion.div
              key={`${object.id}-${i}`}
              layout
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{
                opacity: 1,
                scale: 1,
                backgroundColor: activeIndices.has(i)
                  ? "hsl(var(--primary))"
                  : "hsl(var(--muted))",
                color: activeIndices.has(i)
                  ? "hsl(var(--primary-foreground))"
                  : "hsl(var(--foreground))",
              }}
              exit={{ opacity: 0, scale: 0.5 }}
              transition={{ type: "spring", stiffness: 300, damping: 22 }}
              className="px-3 py-1.5 rounded-full font-mono text-sm"
            >
              {String(val)}
            </motion.div>
          ))}
        </AnimatePresence>
        {values.length === 0 && (
          <div className="px-4 py-2 rounded-lg border border-dashed border-border font-mono text-xs text-muted-foreground">
            ∅
          </div>
        )}
      </div>
    </div>
  );
}

export default memo(SetView);