import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function StackView({ object, events, pointers = [] }) {
  const values = object.value || [];

  const topPointer = pointers.find((p) => p.name === "top");
  const topIndex = topPointer ? topPointer.index : values.length - 1;

  // Active events for the top element
  const isTopActive = useMemo(
    () =>
      events.some(
        (e) =>
          e.type === "Insert" ||
          e.type === "Delete" ||
          e.type === "Pulse" ||
          e.type === "Highlight"
      ),
    [events]
  );

  return (
    <div className="flex flex-col items-center gap-3">
      <Label id={object.id} length={values.length} />
      <div className="flex flex-col-reverse gap-1">
        <AnimatePresence mode="popLayout" initial={false}>
          {values.map((val, i) => {
            const isTop = i === topIndex;
            const isActive = isTop && isTopActive;
            return (
              <motion.div
                key={`${object.id}-${i}`}
                layout
                initial={{ opacity: 0, y: -30 }}
                animate={{
                  opacity: 1,
                  y: 0,
                  backgroundColor: isActive
                    ? "hsl(var(--primary))"
                    : "hsl(var(--muted))",
                  color: isActive
                    ? "hsl(var(--primary-foreground))"
                    : "hsl(var(--foreground))",
                }}
                exit={{ opacity: 0, y: -30 }}
                transition={{ type: "spring", stiffness: 300, damping: 22 }}
                className="w-40 px-4 py-2.5 rounded-lg font-mono text-sm text-center shadow-sm"
              >
                {String(val)}
              </motion.div>
            );
          })}
        </AnimatePresence>
        {values.length === 0 && (
          <div className="w-40 px-4 py-2.5 rounded-lg border border-dashed border-border font-mono text-xs text-muted-foreground text-center">
            empty
          </div>
        )}
      </div>
      <div className="text-[10px] font-mono text-muted-foreground flex items-center gap-1">
        <motion.span
          animate={{ y: isTopActive ? -2 : 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          ↑
        </motion.span>
        <span>top{topIndex >= 0 ? ` (${topIndex})` : ""}</span>
      </div>
    </div>
  );
}

function Label({ id, length }) {
  return (
    <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
      <span className="font-medium">{id}</span>
      <span className="opacity-50">·</span>
      <span>stack · {length}</span>
    </div>
  );
}

export default memo(StackView);