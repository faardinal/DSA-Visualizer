import { useState, useCallback, memo } from "react";
import { AnimatePresence, motion } from "framer-motion";
import VariablesPanel from "./VariablesPanel";
import CodeViewerPanel from "./CodeViewerPanel";
import CallStackPanel from "./CallStackPanel";
import OutputPanel from "./OutputPanel";
import HeapPanel from "./HeapPanel";
import WatchPanel from "./WatchPanel";
import ExecutionStatsPanel from "./ExecutionStatsPanel";
import BreakpointsPanel from "./BreakpointsPanel";
import ExplanationPanel from "./ExplanationPanel";

// ─── palette constants (match index.css dark vars) ─────────────────────────
const C = {
  bg:         "#111111",  // sidebar background
  border:     "#1C1C1C",  // subtle divider
  tabActive:  "#E8E8E8",  // active tab label
  tabInactive:"#555555",  // inactive tab label
  tabHover:   "#888888",
  tabBorder:  "#E8E8E8",  // active bottom indicator
};

// Tabs match old screenshot — short uppercase labels, no icons
const TABS = [
  { id: "variables",   label: "VARS"   },
  { id: "heap",        label: "HEAP"   },
  { id: "callstack",   label: "STACK"  },
  { id: "output",      label: "OUTPUT" },
  { id: "stats",       label: "STATS"  },
  { id: "watch",       label: "WATCH"  },
  { id: "breakpoints", label: "BPS"    },
  { id: "explanation", label: "EXPLAIN"},
  { id: "code",        label: "CODE"   },
];

function Sidebar({
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
  theme,
}) {
  const [activeTab, setActiveTab] = useState("variables");
  const handleTabClick = useCallback((id) => setActiveTab(id), []);

  return (
    <div
      className="h-full flex flex-col overflow-hidden"
      style={{ background: C.bg }}
    >
      {/* ── Tab strip ─────────────────────────────────────────────────── */}
      <div
        className="flex items-end shrink-0 overflow-x-auto"
        style={{
          background: C.bg,
          borderBottom: `1px solid ${C.border}`,
          // hide the horizontal scrollbar on the tab strip itself
          scrollbarWidth: "none",
          msOverflowStyle: "none",
        }}
      >
        {TABS.map(({ id, label }) => {
          const isActive = activeTab === id;
          return (
            <button
              key={id}
              onClick={() => handleTabClick(id)}
              style={{
                flexShrink: 0,
                padding: "7px 9px 6px",
                fontSize: "10px",
                fontWeight: 600,
                letterSpacing: "0.07em",
                lineHeight: 1,
                background: "transparent",
                border: "none",
                borderBottom: `2px solid ${isActive ? C.tabBorder : "transparent"}`,
                color: isActive ? C.tabActive : C.tabInactive,
                cursor: "pointer",
                transition: "color 0.1s, border-color 0.1s",
                whiteSpace: "nowrap",
                // keep the button bottom flush with the strip border
                marginBottom: "-1px",
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.color = C.tabHover;
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.color = C.tabInactive;
              }}
            >
              {label}
            </button>
          );
        })}
      </div>

      {/* ── Tab content ────────────────────────────────────────────────── */}
      {/* flex-1 + min-h-0 so it doesn't grow beyond the sidebar height    */}
      <div className="flex-1 min-h-0 overflow-hidden">
        <AnimatePresence mode="wait">
          {activeTab === "variables" && (
            <ScrollablePanel key="variables">
              <VariablesPanel
                snapshot={snapshot}
                variableDiffs={variableDiffs}
                watchedVars={watchedVars}
                onAddWatch={onAddWatch}
                onRemoveWatch={onRemoveWatch}
              />
            </ScrollablePanel>
          )}

          {activeTab === "code" && (
            <FixedPanel key="code">
              {/*
               * Code tab: Monaco viewer fills the available height, then
               * ExplanationPanel is pinned at the bottom as a fixed-height
               * section. Both read from the same external `explanation` prop
               * — no state is duplicated here.
               */}
              <div className="h-full flex flex-col overflow-hidden">
                {/* Monaco viewer — flex-1 so it fills whatever height remains */}
                <div className="flex-1 min-h-0 overflow-hidden">
                  <CodeViewerPanel
                    code={code}
                    snapshot={snapshot}
                    theme={theme}
                    breakpoints={breakpoints}
                    onToggleBreakpoint={onToggleBreakpoint}
                  />
                </div>
                {/* Explanation pinned at bottom — same prop, single source */}
                <div
                  className="shrink-0"
                  style={{ borderTop: `1px solid ${C.border}`, background: C.bg }}
                >
                  <ExplanationPanel explanation={explanation} compact />
                </div>
              </div>
            </FixedPanel>
          )}

          {activeTab === "callstack" && (
            <ScrollablePanel key="callstack">
              <CallStackPanel snapshot={snapshot} trace={trace} step={step} />
            </ScrollablePanel>
          )}

          {activeTab === "output" && (
            <ScrollablePanel key="output">
              <OutputPanel stdout={stdout} />
            </ScrollablePanel>
          )}

          {activeTab === "heap" && (
            <ScrollablePanel key="heap">
              <HeapPanel snapshot={snapshot} trace={trace} step={step} />
            </ScrollablePanel>
          )}

          {activeTab === "watch" && (
            <ScrollablePanel key="watch">
              <WatchPanel
                snapshot={snapshot}
                watchedVars={watchedVars}
                onRemoveWatch={onRemoveWatch}
              />
            </ScrollablePanel>
          )}

          {activeTab === "stats" && (
            <ScrollablePanel key="stats">
              <ExecutionStatsPanel
                totalSteps={totalSteps}
                executionTime={executionTime}
                demoMode={demoMode}
                trace={trace}
                step={step}
              />
            </ScrollablePanel>
          )}

          {activeTab === "breakpoints" && (
            <ScrollablePanel key="breakpoints">
              <BreakpointsPanel
                breakpoints={breakpoints}
                onToggleBreakpoint={onToggleBreakpoint}
              />
            </ScrollablePanel>
          )}

          {activeTab === "explanation" && (
            <ScrollablePanel key="explanation">
              <ExplanationPanel explanation={explanation} />
            </ScrollablePanel>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

// ── Scrollable panel wrapper: provides the single scroll container ─────────
// All content inside is naturally sized; only this wrapper scrolls.
// This prevents double scrollbars (wrapper + child both scrolling).
function ScrollablePanel({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.1 }}
      style={{
        height: "100%",
        overflowY: "auto",
        overflowX: "hidden",
      }}
    >
      {children}
    </motion.div>
  );
}

// ── Fixed panel wrapper: fills height, NO scroll — content manages itself ──
// Used for the Code tab where Monaco + explanation each own their own height.
function FixedPanel({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.1 }}
      style={{
        height: "100%",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {children}
    </motion.div>
  );
}

export default memo(Sidebar);
