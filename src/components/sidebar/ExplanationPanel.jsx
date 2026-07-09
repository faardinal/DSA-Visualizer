import { Lightbulb } from "lucide-react";

export default function ExplanationPanel({ explanation }) {
  if (!explanation) return null;

  return (
    <div className="px-4 py-3 border-t border-border">
      <div className="flex items-center gap-1.5 mb-2">
        <Lightbulb className="w-3 h-3 text-muted-foreground/60" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
          Explanation
        </span>
      </div>
      <p className="text-xs text-foreground/80 leading-relaxed">{explanation}</p>
    </div>
  );
}