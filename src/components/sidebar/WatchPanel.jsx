import { memo } from "react";
import { Eye, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

function WatchPanel({ snapshot, watchedVars, onRemoveWatch }) {
  const topFrame = snapshot?.locals?.[0];
  const localVars = topFrame?.vars || {};
  const globalVars = snapshot?.globals || {};

  const watched = Array.from(watchedVars || []);

  return (
    <div className="px-4 py-3 h-full overflow-y-auto">
      <div className="flex items-center gap-1.5 mb-2">
        <Eye className="w-3 h-3 text-muted-foreground/60" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
          Watch
        </span>
      </div>
      {watched.length === 0 ? (
        <p className="text-[11px] text-muted-foreground/50 italic">
          Pin variables from the Variables tab
        </p>
      ) : (
        <div className="flex flex-col gap-0.5">
          <AnimatePresence>
            {watched.map((name) => {
              const val = localVars[name] ?? globalVars[name];
              return (
                <motion.div
                  key={name}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                  className="flex items-center gap-2 py-1 text-xs font-mono rounded px-1 hover:bg-muted/40"
                >
                  <span className="text-primary/80 min-w-[40px] truncate">{name}</span>
                  <span className="text-muted-foreground">=</span>
                  {val === undefined ? (
                    <span className="text-muted-foreground/40 italic">—</span>
                  ) : "ref" in val ? (
                    <span className="text-primary/60">{`{${val.ref}}`}</span>
                  ) : (
                    <span className="text-foreground/80">{String(val.value)}</span>
                  )}
                  <button
                    onClick={() => onRemoveWatch(name)}
                    className="ml-auto text-muted-foreground/40 hover:text-destructive transition-colors"
                    title="Unpin"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}

export default memo(WatchPanel);
