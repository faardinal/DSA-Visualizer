import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function LinkedListView({ object, events, pointers = [] }) {
  const nodes = object.value || [];

  const activeIndices = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (typeof e.path === "number") {
        if (["Highlight", "Insert", "Pulse", "Update"].includes(e.type)) {
          set.add(e.path);
        }
      }
    }
    return set;
  }, [events]);

  const headPtr = pointers.find((p) => p.name === "head" || p.name === "current");
  const headIndex = headPtr ? headPtr.index : 0;

  return (
    <div className="flex flex-col items-center gap-3">
      <Label id={object.id} length={nodes.length} />

      {/* Head pointer label */}
      {nodes.length > 0 && (
        <div className="flex gap-0 h-5">
          {nodes.map((_, i) => (
            <div key={`hptr-${i}`} className="flex items-center justify-center" style={{ width: 68 }}>
              {i === headIndex && (
                <span className="text-[10px] font-mono text-primary px-1.5 rounded bg-primary/10">
                  {headPtr?.name || "head"}
                </span>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center">
        <AnimatePresence mode="popLayout" initial={false}>
          {nodes.map((node, i) => {
            const isActive = activeIndices.has(i);
            const val = typeof node === "object" ? (node.value ?? node.val) : node;
            return (
              <motion.div
                key={`${object.id}-${i}`}
                layout
                initial={{ opacity: 0, y: -10, scale: 0.7 }}
                animate={{
                  opacity: 1,
                  y: 0,
                  scale: 1,
                  backgroundColor: isActive
                    ? "hsl(var(--primary))"
                    : "hsl(var(--muted))",
                  color: isActive
                    ? "hsl(var(--primary-foreground))"
                    : "hsl(var(--foreground))",
                }}
                exit={{ opacity: 0, y: 10, scale: 0.7 }}
                transition={{ type: "spring", stiffness: 300, damping: 22 }}
                className="flex items-center"
              >
                <div className="w-16 h-12 flex items-center justify-center rounded-lg font-mono text-sm shadow-sm">
                  {String(val)}
                </div>
                {/* Arrow — animates with node movement via layout */}
                <motion.div
                  layout
                  className="flex items-center"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="w-5 h-px bg-border" />
                  <div className="w-0 h-0 border-l-[6px] border-l-border border-y-[4px] border-y-transparent" />
                </motion.div>
              </motion.div>
            );
          })}
        </AnimatePresence>
        {/* Null terminator */}
        {nodes.length > 0 && (
          <motion.div layout className="flex items-center">
            <div className="w-5 h-px bg-border" />
            <span className="text-[10px] font-mono text-muted-foreground ml-1">null</span>
          </motion.div>
        )}
        {nodes.length === 0 && (
          <div className="px-4 py-3 rounded-lg border border-dashed border-border font-mono text-xs text-muted-foreground">
            empty
          </div>
        )}
      </div>
    </div>
  );
}

function Label({ id, length }) {
  return (
    <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
      <span className="font-medium">{id}</span>
      <span className="opacity-50">·</span>
      <span>linked list · {length}</span>
    </div>
  );
}

export default memo(LinkedListView);