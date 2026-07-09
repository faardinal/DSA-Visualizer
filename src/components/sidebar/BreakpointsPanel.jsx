import { memo } from "react";
import { Circle, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

function BreakpointsPanel({ breakpoints, onToggleBreakpoint, code }) {
  const lines = Array.from(breakpoints || []).sort((a, b) => a - b);
  const codeLines = (code || "").split("\n");

  return (
    <div className="px-4 py-3 h-full overflow-y-auto">
      <div className="flex items-center gap-1.5 mb-2">
        <Circle className="w-3 h-3 fill-destructive text-destructive" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
          Breakpoints
        </span>
      </div>
      {lines.length === 0 ? (
        <p className="text-[11px] text-muted-foreground/50 italic">
          Click line numbers in the editor to set breakpoints
        </p>
      ) : (
        <div className="flex flex-col gap-0.5">
          <AnimatePresence>
            {lines.map((line) => {
              const lineText = codeLines[line - 1]?.trim() || "";
              return (
                <motion.div
                  key={line}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                  className="flex items-center gap-2 py-1 text-xs font-mono rounded px-1 hover:bg-muted/40 cursor-pointer"
                  onClick={() => onToggleBreakpoint(line)}
                >
                  <Circle className="w-2.5 h-2.5 fill-destructive text-destructive shrink-0" />
                  <span className="text-muted-foreground/60 min-w-[2rem]">L{line}</span>
                  <span className="text-foreground/70 truncate flex-1">{lineText || "—"}</span>
                  <button
                    className="ml-auto text-muted-foreground/40 hover:text-destructive transition-colors"
                    title="Remove breakpoint"
                    onClick={(e) => { e.stopPropagation(); onToggleBreakpoint(line); }}
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

export default memo(BreakpointsPanel);
