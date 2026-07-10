import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function QueueView({ object, events, pointers = [] }) {
  const values = object.value || [];

  const frontPtr = pointers.find((p) => p.name === "front");
  const rearPtr = pointers.find((p) => p.name === "rear");
  const frontIndex = frontPtr ? frontPtr.index : 0;
  const rearIndex = rearPtr ? rearPtr.index : values.length - 1;

  const activeEnds = useMemo(
    () => events.some((e) => ["Insert", "Delete", "Pulse", "Highlight"].includes(e.type)),
    [events]
  );

  const insertedAtEnd = useMemo(
    () =>
      events.some(
        (e) =>
          e.type === "Insert" &&
          (typeof e.path === "number" ? e.path === values.length - 1 : false)
      ),
    [events, values.length]
  );

  return (
    <div className="flex flex-col items-center gap-3">
      <Label id={object.id} length={values.length} />
      <div className="flex items-center gap-1">
        {/* Front pointer */}
        <div className="flex flex-col items-center justify-center min-w-[36px]">
          {values.length > 0 && (
            <>
              <span className="text-[10px] font-mono text-primary px-1 rounded bg-primary/10 leading-tight">
                front
              </span>
              <span className="text-primary text-xs">↓</span>
            </>
          )}
        </div>

        <div className="flex gap-1">
          <AnimatePresence mode="popLayout" initial={false}>
            {values.map((val, i) => {
              const isFront = i === frontIndex;
              const isRear = i === rearIndex;
              const isActive = activeEnds && (isFront || isRear);
              const isNew = insertedAtEnd && isRear;
              return (
                <motion.div
                  key={`${object.id}-${i}`}
                  layout
                  initial={{ opacity: 0, x: 30, scale: 0.7 }}
                  animate={{
                    opacity: 1,
                    x: 0,
                    scale: 1,
                    backgroundColor: isActive
                      ? "hsl(var(--primary))"
                      : "hsl(var(--muted))",
                    color: isActive
                      ? "hsl(var(--primary-foreground))"
                      : "hsl(var(--foreground))",
                  }}
                  exit={{ opacity: 0, x: -30, scale: 0.7 }}
                  transition={{ type: "spring", stiffness: 300, damping: 22 }}
                  className="w-12 h-10 flex items-center justify-center rounded-lg font-mono text-sm shadow-sm"
                >
                  {String(val)}
                </motion.div>
              );
            })}
          </AnimatePresence>
          {values.length === 0 && (
            <div className="w-12 h-10 flex items-center justify-center rounded-lg border border-dashed border-border font-mono text-xs text-muted-foreground">
              ∅
            </div>
          )}
        </div>

        {/* Rear pointer */}
        <div className="flex flex-col items-center justify-center min-w-[36px]">
          {values.length > 0 && (
            <>
              <span className="text-[10px] font-mono text-primary px-1 rounded bg-primary/10 leading-tight">
                rear
              </span>
              <span className="text-primary text-xs">↓</span>
            </>
          )}
        </div>
      </div>
      <div className="flex items-center gap-12 text-[10px] font-mono text-muted-foreground">
        <span>← dequeue</span>
        <span>enqueue →</span>
      </div>
    </div>
  );
}

function Label({ id, length }) {
  return (
    <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
      <span className="font-medium">{id}</span>
      <span className="opacity-50">·</span>
      <span>queue · {length}</span>
    </div>
  );
}

export default memo(QueueView);