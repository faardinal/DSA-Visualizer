import { memo } from "react";
import { motion, AnimatePresence } from "framer-motion";

// Works both as a standalone panel (original) and as tab content (showAlways=true)
function CallStackPanel({ snapshot, showAlways = false }) {
  if (!snapshot || !snapshot.locals) return null;
  if (!showAlways && snapshot.locals.length <= 1) return null;

  const isReturning = snapshot.event === "return" && snapshot.returnValue !== undefined;

  return (
    <div>
      <PanelHeader title="Call Stack" />
      <div className="flex flex-col gap-0.5 mt-2">
        <AnimatePresence initial={false}>
          {snapshot.locals.map((frame, i) => (
            <motion.div
              key={frame.frame_id}
              layout
              initial={{ opacity: 0, x: -20, height: 0 }}
              animate={{ opacity: 1, x: 0, height: "auto" }}
              exit={{ opacity: 0, x: 20, height: 0 }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
              className={`flex items-center gap-2 py-1 text-xs font-mono overflow-hidden ${
                i === 0 ? "text-foreground" : "text-muted-foreground"
              }`}
            >
              {i === 0 && (
                <motion.span
                  layoutId="callstack-active"
                  className="w-1.5 h-1.5 rounded-full bg-primary shrink-0"
                />
              )}
              {i !== 0 && <span className="w-1.5 h-1.5 shrink-0" />}
              <span>{frame.func}</span>
              <span className="text-muted-foreground/50 text-[10px]">{frame.frame_id}</span>
              {i === 0 && isReturning && (
                <span className="text-[10px] text-primary ml-auto">↩ returning</span>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}

function PanelHeader({ title }) {
  return (
    <div className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
      {title}
    </div>
  );
}

export default memo(CallStackPanel);
