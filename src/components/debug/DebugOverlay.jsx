import { Bug, X } from "lucide-react";

export default function DebugOverlay({ snapshot, events, step, maxStep, onClose }) {
  if (!snapshot) return null;

  return (
    <div className="absolute bottom-4 left-4 right-4 z-50 glass-subtle rounded-xl shadow-macos border border-border overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-muted/30">
        <div className="flex items-center gap-2">
          <Bug className="w-3.5 h-3.5 text-primary" />
          <span className="text-xs font-medium">Debug Mode</span>
          <span className="text-[10px] font-mono text-muted-foreground">
            step {step}/{maxStep}
          </span>
        </div>
        <button onClick={onClose} className="p-1 rounded-md hover:bg-muted text-muted-foreground">
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
      <div className="grid grid-cols-3 gap-px bg-border max-h-64 overflow-auto">
        <DebugSection title="Snapshot JSON">
          <pre className="text-[10px] font-mono text-foreground/80 leading-relaxed overflow-auto">
            {JSON.stringify(snapshot, null, 2)}
          </pre>
        </DebugSection>
        <DebugSection title="Diff Events">
          <pre className="text-[10px] font-mono text-foreground/80 leading-relaxed overflow-auto">
            {events.length > 0 ? JSON.stringify(events, null, 2) : "No changes from previous step."}
          </pre>
        </DebugSection>
        <DebugSection title="Heap Objects">
          <div className="flex flex-col gap-1">
            {snapshot.heap?.map((obj) => (
              <div key={obj.id} className="text-[10px] font-mono">
                <span className="text-primary">{obj.id}</span>
                <span className="text-muted-foreground"> · {obj.type}</span>
              </div>
            ))}
          </div>
        </DebugSection>
      </div>
    </div>
  );
}

function DebugSection({ title, children }) {
  return (
    <div className="bg-background p-3 overflow-auto">
      <div className="text-[9px] font-semibold uppercase tracking-wider text-muted-foreground/60 mb-2">
        {title}
      </div>
      {children}
    </div>
  );
}