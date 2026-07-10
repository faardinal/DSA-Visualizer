import { memo, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

const CELL_SIZE = 48; // w-12
const GAP = 6; // gap-1.5

function ArrayView({ object, events, pointers = [] }) {
  const values = object.value || [];
  const isTuple = object.type === "tuple";

  // Active indices from events (Swap, Update, Insert, Delete, Highlight, Pulse)
  const eventIndices = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Swap" && e.metadata) {
        set.add(e.metadata.i);
        set.add(e.metadata.j);
      } else if (typeof e.path === "number") {
        if (["Highlight", "Insert", "Pulse", "Update", "Delete"].includes(e.type)) {
          set.add(e.path);
        }
      }
    }
    return set;
  }, [events]);

  // Swap pairs — for lift animation
  const swapIndices = useMemo(() => {
    const set = new Set();
    for (const e of events) {
      if (e.type === "Swap" && e.metadata) {
        set.add(e.metadata.i);
        set.add(e.metadata.j);
      }
    }
    return set;
  }, [events]);

  // Pointers grouped by index — stack cleanly without overlap
  const pointersByIndex = useMemo(() => {
    const map = {};
    for (const p of pointers) {
      if (p.index >= 0 && p.index < values.length) {
        if (!map[p.index]) map[p.index] = [];
        map[p.index].push(p.name);
      }
    }
    return map;
  }, [pointers, values.length]);

  // Selected range (left..right or low..high) — subtle background
  const range = useMemo(() => {
    const left = pointers.find((p) => p.name === "left" || p.name === "low");
    const right = pointers.find((p) => p.name === "right" || p.name === "high");
    if (left && right) {
      return {
        start: Math.min(left.index, right.index),
        end: Math.max(left.index, right.index),
      };
    }
    return null;
  }, [pointers]);

  return (
    <div className="flex flex-col items-center gap-1.5">
      <Label id={object.id} type={object.type} length={values.length} />

      {/* Pointer labels row — stacked vertically per index */}
      <div className="flex gap-1.5 min-h-[28px] items-end">
        {values.map((_, i) => (
          <div key={`ptr-${i}`} className="w-12 flex flex-col items-center justify-end gap-0.5">
            {(pointersByIndex[i] || []).map((name) => (
              <span
                key={name}
                className="text-[10px] font-mono text-primary px-1.5 rounded bg-primary/10 leading-tight"
              >
                {name}
              </span>
            ))}
          </div>
        ))}
      </div>

      {/* Arrow row */}
      <div className="flex gap-1.5 min-h-[16px]">
        {values.map((_, i) => (
          <div key={`arr-${i}`} className="w-12 flex justify-center">
            {pointersByIndex[i] && <span className="text-primary text-xs">↓</span>}
          </div>
        ))}
      </div>

      {/* Value boxes with optional range background */}
      <div className="flex gap-1.5 relative">
        {range && values.length > 0 && (
          <div
            className="absolute top-0 bottom-0 bg-primary/5 rounded-lg pointer-events-none"
            style={{
              left: range.start * (CELL_SIZE + GAP) - GAP / 2,
              width: (range.end - range.start + 1) * (CELL_SIZE + GAP) - GAP,
            }}
          />
        )}
        <AnimatePresence mode="popLayout" initial={false}>
          {values.map((val, i) => {
            const isActive = eventIndices.has(i);
            const isSwap = swapIndices.has(i);
            return (
              <motion.div
                key={`${object.id}-${i}`}
                layout
                initial={{ opacity: 0, scale: 0.7, y: -10 }}
                animate={{
                  opacity: 1,
                  scale: 1,
                  y: isSwap ? -8 : 0,
                  backgroundColor: isActive
                    ? "hsl(var(--primary))"
                    : "hsl(var(--muted))",
                  color: isActive
                    ? "hsl(var(--primary-foreground))"
                    : "hsl(var(--foreground))",
                }}
                exit={{ opacity: 0, scale: 0.7, y: 10 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                className={`w-12 h-12 flex items-center justify-center font-mono text-sm font-medium shadow-sm relative z-10 ${
                  isTuple
                    ? "rounded-none border-2 border-dashed border-current/40"
                    : "rounded-lg"
                }`}
              >
                {formatValue(val)}
              </motion.div>
            );
          })}
        </AnimatePresence>
        {isTuple && values.length > 0 && (
          <>
            <span className="absolute -left-3 top-1/2 -translate-y-1/2 text-lg text-muted-foreground font-mono pointer-events-none">(</span>
            <span
              className="absolute -translate-y-1/2 top-1/2 text-lg text-muted-foreground font-mono pointer-events-none"
              style={{ left: values.length * (CELL_SIZE + GAP) - GAP + 4 }}
            >)</span>
          </>
        )}
        {values.length === 0 && (
          <div
            className={`w-12 h-12 flex items-center justify-center border border-dashed border-border font-mono text-xs text-muted-foreground ${
              isTuple ? "rounded-none" : "rounded-lg"
            }`}
          >
            {isTuple ? "()" : "∅"}
          </div>
        )}
      </div>

      {/* Index labels */}
      <div className="flex gap-1.5">
        {values.map((_, i) => (
          <div
            key={`idx-${i}`}
            className="w-12 text-center text-[10px] font-mono text-muted-foreground"
          >
            {i}
          </div>
        ))}
      </div>
    </div>
  );
}

function formatValue(val) {
  if (val === null || val === undefined) return "null";
  if (typeof val === "object") return JSON.stringify(val);
  return String(val);
}

function Label({ id, type, length }) {
  return (
    <div className="flex items-center gap-2 text-[11px] font-mono text-muted-foreground">
      <span className="font-medium">{id}</span>
      <span className="opacity-50">·</span>
      <span>{type}</span>
      <span className="opacity-50">·</span>
      <span>len {length}</span>
    </div>
  );
}

export default memo(ArrayView);