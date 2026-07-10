import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

// Generic fallback renderer for heap objects whose type doesn't match a
// dedicated renderer (e.g. custom Python classes like `Node`, `TreeNode`,
// or anything else with a `__dict__`). Without this, VisualizationCanvas
// silently dropped these objects entirely — the most common cause of
// "nothing shows up" when tracing code that uses classes.
function ObjectView({ object, events = [] }) {
  const entries = useMemo(() => Object.entries(object.value || {}), [object.value]);

  const activeKeys = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (typeof e.path === "string") set.add(e.path);
      else if (e.path == null) entries.forEach(([k]) => set.add(k));
    }
    return set;
  }, [events, entries]);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
        <span className="font-medium">{object.id}</span>
        <span className="opacity-50">·</span>
        <span>{object.type}</span>
      </div>
      <div className="flex flex-col gap-1 min-w-[180px] rounded-lg border border-border p-2">
        <AnimatePresence mode="popLayout" initial={false}>
          {entries.map(([key, val]) => {
            const isActive = activeKeys.has(key);
            const isRef = val !== null && typeof val === "object" && "ref" in val;
            return (
              <motion.div
                key={key}
                layout
                initial={{ opacity: 0 }}
                animate={{
                  opacity: 1,
                  backgroundColor: isActive
                    ? "hsl(var(--primary) / 0.12)"
                    : "hsl(var(--background) / 0)",
                }}
                transition={{ duration: 0.5 }}
                className="flex items-center gap-2 px-2 py-1 rounded text-xs font-mono"
              >
                <span className="text-primary/80">{key}</span>
                <span className="text-muted-foreground">=</span>
                {isRef ? (
                  <span className="text-primary/60">{`{${val.ref}}`}</span>
                ) : (
                  <span className="text-foreground/80">{formatValue(val)}</span>
                )}
              </motion.div>
            );
          })}
        </AnimatePresence>
        {entries.length === 0 && (
          <span className="text-[11px] text-muted-foreground/50 italic px-2 py-1">no attributes</span>
        )}
      </div>
    </div>
  );
}

function formatValue(val) {
  if (val === null || val === undefined) return "null";
  if (typeof val === "object") return JSON.stringify(val);
  return String(val);
}

export default memo(ObjectView);
