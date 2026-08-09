import { Lightbulb } from "lucide-react";

/**
 * ExplanationPanel — reusable explanation block.
 *
 * Rendered in two places:
 *   1. The dedicated "EXPLAIN" tab (standalone scroll)
 *   2. The bottom of the "CODE" tab (below the code viewer)
 *
 * Same component, same `explanation` prop, same state — single source of truth.
 */
export default function ExplanationPanel({ explanation }) {
  if (!explanation) {
    return (
      <div className="px-3 py-3">
        <div className="flex items-center gap-1.5 mb-1.5">
          <Lightbulb className="w-3 h-3" style={{ color: "#4A4A4A" }} />
          <span
            className="font-semibold uppercase tracking-wider"
            style={{ fontSize: "9px", color: "#4A4A4A" }}
          >
            Explanation
          </span>
        </div>
        <p style={{ fontSize: "11px", color: "#555555", lineHeight: 1.5 }}>
          Run code to see step-by-step explanations here.
        </p>
      </div>
    );
  }

  return (
    <div className="px-3 py-3">
      <div className="flex items-center gap-1.5 mb-1.5">
        <Lightbulb className="w-3 h-3" style={{ color: "#9A9A9A" }} />
        <span
          className="font-semibold uppercase tracking-wider"
          style={{ fontSize: "9px", color: "#9A9A9A" }}
        >
          Explanation
        </span>
      </div>
      <p style={{ fontSize: "11px", color: "#C8C8C8", lineHeight: 1.65 }}>
        {explanation}
      </p>
    </div>
  );
}
