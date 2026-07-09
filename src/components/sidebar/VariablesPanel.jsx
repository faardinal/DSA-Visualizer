import { memo } from "react";
import { motion } from "framer-motion";
import { Pin } from "lucide-react";

function VariablesPanel({ snapshot, variableDiffs = {}, watchedVars, onAddWatch, onRemoveWatch }) {
  const topFrame = snapshot?.locals?.[0];
  const localVars = topFrame?.vars || {};
  const globalVars = snapshot?.globals || {};

  if (!snapshot) return null;

  const hasReturn = snapshot.event === "return" && snapshot.returnValue !== undefined;

  return (
    <div className="px-4 py-3 h-full overflow-y-auto">
      <PanelHeader title="Variables" />
      <div className="flex flex-col gap-0.5 mt-2">
        {Object.entries(localVars).map(([name, val]) => (
          <VarRow
            key={`l-${name}`}
            name={name}
            val={val}
            diff={variableDiffs[name]}
            isPinned={watchedVars?.has(name)}
            onPin={() => watchedVars?.has(name) ? onRemoveWatch?.(name) : onAddWatch?.(name)}
          />
        ))}
        {Object.keys(localVars).length === 0 && (
          <span className="text-[11px] text-muted-foreground/50 italic">No local variables</span>
        )}
      </div>
      {hasReturn && (
        <motion.div
          initial={{ opacity: 0, y: -6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="flex items-center gap-2 py-1.5 px-1 mt-2 text-xs font-mono rounded bg-primary/10"
        >
          <span className="text-primary">↩ returns</span>
          <span className="text-foreground/80">
            {"ref" in snapshot.returnValue
              ? `{${snapshot.returnValue.ref}}`
              : String(snapshot.returnValue.value)}
          </span>
          {!("ref" in snapshot.returnValue) && snapshot.returnValue.value === null && (
            <span className="text-[10px] text-muted-foreground/50 italic">
              (explicit `return None` and falling off the end look the same to the tracer)
            </span>
          )}
        </motion.div>
      )}
      {Object.keys(globalVars).length > 0 && (
        <>
          <PanelHeader title="Globals" className="mt-3" />
          <div className="flex flex-col gap-0.5 mt-2">
            {Object.entries(globalVars).map(([name, val]) => (
              <VarRow
                key={`g-${name}`}
                name={name}
                val={val}
                isPinned={watchedVars?.has(name)}
                onPin={() => watchedVars?.has(name) ? onRemoveWatch?.(name) : onAddWatch?.(name)}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function VarRow({ name, val, diff, isPinned, onPin }) {
  const isRef = "ref" in val;
  const hasChanged = diff && diff.change === "changed";
  const wasAdded = diff && diff.change === "added";

  return (
    <motion.div
      initial={wasAdded ? { opacity: 0, x: -10 } : false}
      animate={{
        opacity: 1,
        x: 0,
        backgroundColor: hasChanged
          ? "hsl(var(--primary) / 0.1)"
          : "hsl(var(--background) / 0)",
      }}
      transition={{ duration: 0.6 }}
      className="group flex items-center gap-2 py-1 text-xs font-mono rounded px-1"
      title={isRef ? `→ ${val.ref}` : undefined}
    >
      <span className="text-primary/80 min-w-[40px] truncate">{name}</span>
      <span className="text-muted-foreground">=</span>
      {isRef ? (
        <span className="text-primary/60 cursor-pointer hover:text-primary transition-colors">
          {`{${val.ref}}`}
        </span>
      ) : (
        <span className="text-foreground/80">{String(val.value)}</span>
      )}
      {hasChanged && (
        <motion.span
          initial={{ opacity: 1 }}
          animate={{ opacity: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="text-primary text-[9px]"
        >
          ●
        </motion.span>
      )}
      {onPin && (
        <button
          onClick={onPin}
          className={`ml-auto opacity-0 group-hover:opacity-100 transition-opacity ${
            isPinned ? "!opacity-100 text-primary" : "text-muted-foreground/40 hover:text-primary"
          }`}
          title={isPinned ? "Unpin" : "Pin to Watch"}
        >
          <Pin className="w-3 h-3" />
        </button>
      )}
    </motion.div>
  );
}

function PanelHeader({ title, className = "" }) {
  return (
    <div className={`text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60 ${className}`}>
      {title}
    </div>
  );
}

export default memo(VariablesPanel);
