import { Terminal } from "lucide-react";

export default function OutputPanel({ stdout }) {
  return (
    <div className="px-4 py-3 h-full overflow-y-auto">
      <div className="flex items-center gap-1.5 mb-2">
        <Terminal className="w-3 h-3 text-muted-foreground/60" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
          Output
        </span>
      </div>
      {stdout ? (
        <pre className="text-xs font-mono text-foreground/80 whitespace-pre-wrap leading-relaxed">
          {stdout}
        </pre>
      ) : (
        <span className="text-[11px] text-muted-foreground/50 italic">No output yet</span>
      )}
    </div>
  );
}
