import { memo, useMemo } from "react";
import { Gauge } from "lucide-react";

function ExecutionStatsPanel({ totalSteps, executionTime, demoMode, trace, step }) {
  const stats = useMemo(() => {
    if (!trace || !trace.length) return null;

    let objectsCreated = 0;
    let functionsCalled = 0;
    let peakRecursion = 0;
    let peakHeapObjects = 0;
    const seenHeapIds = new Set();

    for (let i = 0; i < trace.length; i++) {
      const snap = trace[i];
      const prev = i > 0 ? trace[i - 1] : null;

      // Peak recursion = max call stack depth
      const depth = snap.locals?.length ?? 1;
      if (depth > peakRecursion) peakRecursion = depth;

      // Functions called = steps where depth increased (a call event)
      const prevDepth = prev?.locals?.length ?? 1;
      if (depth > prevDepth) functionsCalled++;

      // Objects created = new heap IDs that haven't appeared before
      for (const obj of snap.heap || []) {
        if (!seenHeapIds.has(String(obj.id))) {
          seenHeapIds.add(String(obj.id));
          objectsCreated++;
        }
      }

      // Peak heap objects (count of SKIP-filtered items per snapshot)
      const heapCount = (snap.heap || []).filter(
        (o) => !["function", "unsupported", "module", "type"].includes(o.type)
      ).length;
      if (heapCount > peakHeapObjects) peakHeapObjects = heapCount;
    }

    return { objectsCreated, functionsCalled, peakRecursion, peakHeapObjects };
  }, [trace]);

  const currentSnap = trace?.[step];
  const currentVarsCount = currentSnap
    ? Object.keys(currentSnap.locals?.[0]?.vars || {}).length
    : 0;
  const currentHeapCount = (currentSnap?.heap || []).filter(
    (o) => !["function", "unsupported", "module", "type"].includes(o.type)
  ).length;

  if (!totalSteps) return null;

  return (
    <div className="px-4 py-3 h-full overflow-y-auto">
      <div className="flex items-center gap-1.5 mb-3">
        <Gauge className="w-3 h-3 text-muted-foreground/60" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
          Statistics
        </span>
        <span className="ml-auto text-[9px] text-muted-foreground/40">{demoMode ? "sample trace" : "live run"}</span>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <StatRow label="Steps" value={totalSteps} />
        <StatRow label="Exec Time" value={executionTime != null ? formatTime(executionTime) : "—"} />
        <StatRow label="Objects Created" value={stats?.objectsCreated ?? "—"} />
        <StatRow label="Functions Called" value={stats?.functionsCalled ?? "—"} />
        <StatRow label="Peak Heap Objects" value={stats?.peakHeapObjects ?? "—"} />
        <StatRow label="Peak Recursion" value={stats?.peakRecursion ?? "—"} />
        <StatRow label="Variables (now)" value={currentVarsCount} />
        <StatRow label="Heap Objects (now)" value={currentHeapCount} />
      </div>
    </div>
  );
}

function StatRow({ label, value }) {
  return (
    <div className="flex flex-col gap-0.5 bg-muted/20 rounded-md px-2 py-1.5">
      <span className="text-[9px] text-muted-foreground/50 uppercase tracking-wider">{label}</span>
      <span className="text-xs font-mono font-semibold text-foreground/80">{String(value)}</span>
    </div>
  );
}

function formatTime(seconds) {
  if (seconds < 0.001) return "<1ms";
  if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
  return `${seconds.toFixed(2)}s`;
}

export default memo(ExecutionStatsPanel);
