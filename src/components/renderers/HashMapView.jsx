import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function HashMapView({ object, events }) {
  const entries = useMemo(
    () => Object.entries(object.value || {}),
    [object.value]
  );

  // Active keys — pulse only changed entry, never rerender entire map
  const activeKeys = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (typeof e.path === "string") {
        if (["Pulse", "Insert", "Update", "Highlight", "Delete"].includes(e.type)) {
          set.add(e.path);
        }
      }
    }
    return set;
  }, [events]);

  const insertedKeys = useMemo(
    () =>
      new Set(
        events.filter((e) => e.type === "Insert" && typeof e.path === "string").map((e) => e.path)
      ),
    [events]
  );

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
        <span className="font-medium">{object.id}</span>
        <span className="opacity-50">·</span>
        <span>dict · {entries.length} entries</span>
      </div>
      <div className="flex flex-col gap-1.5 min-w-[200px]">
        <AnimatePresence mode="popLayout" initial={false}>
          {entries.map(([key, val]) => {
            const isActive = activeKeys.has(key);
            const isNew = insertedKeys.has(key);
            return (
              <motion.div
                key={key}
                layout
                initial={{ opacity: 0, y: -8, scale: 0.95 }}
                animate={{
                  opacity: 1,
                  y: 0,
                  scale: 1,
                  backgroundColor: isActive
                    ? "hsl(var(--primary) / 0.15)"
                    : "hsl(var(--muted))",
                  boxShadow: isActive
                    ? "inset 0 0 0 1px hsl(var(--primary))"
                    : "inset 0 0 0 1px hsl(var(--border))",
                }}
                exit={{ opacity: 0, y: -8, scale: 0.95 }}
                transition={{ type: "spring", stiffness: 300, damping: 22 }}
                className="flex items-center gap-3 px-4 py-2.5 rounded-lg"
              >
                <span className="font-mono text-sm font-medium text-foreground min-w-[32px]">
                  {key}
                </span>
                <span className="text-muted-foreground text-xs">→</span>
                <motion.span
                  key={String(val)}
                  initial={isNew ? { scale: 0.5 } : false}
                  animate={{ scale: 1 }}
                  className="font-mono text-sm text-foreground/80"
                >
                  {formatValue(val)}
                </motion.span>
              </motion.div>
            );
          })}
        </AnimatePresence>
        {entries.length === 0 && (
          <div className="px-4 py-2.5 rounded-lg border border-dashed border-border font-mono text-xs text-muted-foreground text-center min-w-[200px]">
            empty
          </div>
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

export default memo(HashMapView);