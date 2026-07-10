import { AlertTriangle } from "lucide-react";
import { motion } from "framer-motion";

// Shown whenever the current snapshot is an 'exception' event
export default function ExceptionPanel({ exception, snapshot }) {
  if (!exception) return null;

  const callStack = snapshot?.locals || [];

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      className="px-4 py-3 border-t border-destructive/30 bg-destructive/10"
    >
      <div className="flex items-center gap-1.5 mb-1.5">
        <AlertTriangle className="w-3.5 h-3.5 text-destructive" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-destructive">
          {exception.type || "Exception"}
        </span>
        {(exception.line ?? snapshot?.line) != null && (
          <span className="text-[10px] font-mono text-destructive/70 ml-auto">
            line {exception.line ?? snapshot?.line}
          </span>
        )}
      </div>
      <p className="text-xs font-mono text-destructive/90 leading-relaxed break-words mb-2">
        {exception.message}
      </p>
      {callStack.length > 0 && (
        <div className="mt-2">
          <div className="text-[9px] font-semibold uppercase tracking-wider text-destructive/60 mb-1">
            Stack at exception:
          </div>
          <div className="flex flex-col gap-0.5">
            {callStack.map((frame, i) => (
              <div key={frame.frame_id ?? i} className="flex items-center gap-1.5 text-[10px] font-mono text-destructive/70">
                <span className="w-1.5 h-1.5 rounded-full bg-destructive/40 shrink-0" />
                <span>{frame.func}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}
