import { useState, useCallback, memo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Variable,
  Code2,
  Layers,
  Terminal,
  Database,
  Eye,
  Gauge,
  GitBranch,
  Lightbulb,
} from "lucide-react";
import VariablesPanel from "./VariablesPanel";
import CodeViewerPanel from "./CodeViewerPanel";
import CallStackPanel from "./CallStackPanel";
import OutputPanel from "./OutputPanel";
import HeapPanel from "./HeapPanel";
import WatchPanel from "./WatchPanel";
import ExecutionStatsPanel from "./ExecutionStatsPanel";
import BreakpointsPanel from "./BreakpointsPanel";
import ExplanationPanel from "./ExplanationPanel";

const TABS = [
  { id: "variables", label: "Variables", Icon: Variable },
  { id: "code", label: "Code", Icon: Code2 },
  { id: "callstack", label: "Call Stack", Icon: Layers },
  { id: "output", label: "Output", Icon: Terminal },
  { id: "heap", label: "Heap", Icon: Database },
  { id: "watch", label: "Watch", Icon: Eye },
  { id: "stats", label: "Stats", Icon: Gauge },
  { id: "breakpoints", label: "Breakpoints", Icon: GitBranch },
  { id: "explanation", label: "Explain", Icon: Lightbulb },
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

  const handleTabClick = useCallback((tabId) => {
    setActiveTab(tabId);
  }, []);

  return (
    <div className="h-full flex flex-col bg-sidebar text-foreground overflow-hidden">
      {/* Tab strip */}
      <div className="flex items-center border-b border-border overflow-x-auto shrink-0 no-scrollbar">
        {TABS.map(({ id, label, Icon }) => (
          <button
            key={id}
            onClick={() => handleTabClick(id)}
            className={`
              flex items-center gap-1 px-2.5 py-1.5 text-[10px] font-medium
              whitespace-nowrap transition-colors shrink-0 border-b-2
              ${
                activeTab === id
                  ? "border-primary text-foreground bg-primary/5"
                  : "border-transparent text-muted-foreground hover:text-foreground hover:bg-muted/50"
              }
            `}
          >
            <Icon className="w-3 h-3" />
            {label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="flex-1 min-h-0 overflow-hidden">
        <AnimatePresence mode="wait">
          {activeTab === "variables" && (
            <TabPanel key="variables">
              <VariablesPanel
                snapshot={snapshot}
                variableDiffs={variableDiffs}
                watchedVars={watchedVars}
                onAddWatch={onAddWatch}
                onRemoveWatch={onRemoveWatch}
              />
            </TabPanel>
          )}
          {activeTab === "code" && (
            <TabPanel key="code">
              <CodeViewerPanel
                code={code}
                snapshot={snapshot}
                theme={theme}
                breakpoints={breakpoints}
                onToggleBreakpoint={onToggleBreakpoint}
              />
            </TabPanel>
          )}
          {activeTab === "callstack" && (
            <TabPanel key="callstack">
              <CallStackPanel snapshot={snapshot} trace={trace} step={step} />
            </TabPanel>
          )}
          {activeTab === "output" && (
            <TabPanel key="output">
              <OutputPanel stdout={stdout} />
            </TabPanel>
          )}
          {activeTab === "heap" && (
            <TabPanel key="heap">
              <HeapPanel snapshot={snapshot} trace={trace} step={step} />
            </TabPanel>
          )}
          {activeTab === "watch" && (
            <TabPanel key="watch">
              <WatchPanel
                snapshot={snapshot}
                watchedVars={watchedVars}
                onRemoveWatch={onRemoveWatch}
              />
            </TabPanel>
          )}
          {activeTab === "stats" && (
            <TabPanel key="stats">
              <ExecutionStatsPanel
                totalSteps={totalSteps}
                executionTime={executionTime}
                demoMode={demoMode}
                trace={trace}
                step={step}
              />
            </TabPanel>
          )}
          {activeTab === "breakpoints" && (
            <TabPanel key="breakpoints">
              <BreakpointsPanel
                breakpoints={breakpoints}
                onToggleBreakpoint={onToggleBreakpoint}
              />
            </TabPanel>
          )}
          {activeTab === "explanation" && (
            <TabPanel key="explanation">
              <ExplanationPanel explanation={explanation} />
            </TabPanel>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function TabPanel({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -4 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 4 }}
      transition={{ duration: 0.15 }}
      className="h-full overflow-y-auto"
    >
      {children}
    </motion.div>
  );
}

export default memo(Sidebar);
