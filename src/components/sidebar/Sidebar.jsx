import { useState } from "react";
import VariablesPanel from "./VariablesPanel";
import CallStackPanel from "./CallStackPanel";
import ExplanationPanel from "./ExplanationPanel";
import OutputPanel from "./OutputPanel";
import ExceptionPanel from "./ExceptionPanel";
import ExecutionStatsPanel from "./ExecutionStatsPanel";
import WatchPanel from "./WatchPanel";
import BreakpointsPanel from "./BreakpointsPanel";
import HeapPanel from "./HeapPanel";

const TABS = [
  { id: "variables", label: "Vars" },
  { id: "heap", label: "Heap" },
  { id: "callstack", label: "Stack" },
  { id: "output", label: "Output" },
  { id: "stats", label: "Stats" },
  { id: "watch", label: "Watch" },
  { id: "breakpoints", label: "BPs" },
];

export default function Sidebar({
  code,
  snapshot,
  explanation,
  stdout,
  variableDiffs,
  totalSteps,
  executionTime,
  demoMode,
  trace,
  step,
  watchedVars,
  onAddWatch,
  onRemoveWatch,
  breakpoints,
  onToggleBreakpoint,
  events,
}) {
  const [activeTab, setActiveTab] = useState("variables");
  const isException = snapshot?.event === "exception";

  return (
    <div className="h-full flex flex-col bg-sidebar">
      {/* Exception banner — always visible regardless of tab */}
      {isException && (
        <ExceptionPanel
          exception={snapshot.exception}
          snapshot={snapshot}
        />
      )}

      {/* Tab bar */}
      <div className="flex items-center border-b border-border overflow-x-auto shrink-0 bg-sidebar">
        {TABS.map((tab) => {
          const badgeCount =
            tab.id === "watch" ? (watchedVars?.size || 0) :
            tab.id === "breakpoints" ? (breakpoints?.size || 0) :
            null;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`relative px-2.5 py-2 text-[10px] font-semibold uppercase tracking-wider whitespace-nowrap transition-colors shrink-0 ${
                activeTab === tab.id
                  ? "text-primary border-b-2 border-primary -mb-px"
                  : "text-muted-foreground/60 hover:text-muted-foreground"
              }`}
            >
              {tab.label}
              {badgeCount != null && badgeCount > 0 && (
                <span className="ml-0.5 text-[8px] text-primary font-bold">{badgeCount}</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === "variables" && (
          <VariablesPanel
            snapshot={snapshot}
            variableDiffs={variableDiffs}
            watchedVars={watchedVars}
            onAddWatch={onAddWatch}
            onRemoveWatch={onRemoveWatch}
          />
        )}
        {activeTab === "heap" && (
          <HeapPanel snapshot={snapshot} events={events} />
        )}
        {activeTab === "callstack" && (
          <div className="px-4 py-3">
            <CallStackPanel snapshot={snapshot} showAlways={true} />
            {explanation && (
              <div className="mt-4">
                <ExplanationPanel explanation={explanation} />
              </div>
            )}
          </div>
        )}
        {activeTab === "output" && (
          <OutputPanel stdout={stdout} />
        )}
        {activeTab === "stats" && (
          <ExecutionStatsPanel
            totalSteps={totalSteps}
            executionTime={executionTime}
            demoMode={demoMode}
            trace={trace}
            step={step}
          />
        )}
        {activeTab === "watch" && (
          <WatchPanel
            snapshot={snapshot}
            watchedVars={watchedVars}
            onRemoveWatch={onRemoveWatch}
          />
        )}
        {activeTab === "breakpoints" && (
          <BreakpointsPanel
            breakpoints={breakpoints}
            onToggleBreakpoint={onToggleBreakpoint}
            code={code}
          />
        )}
      </div>
    </div>
  );
}
