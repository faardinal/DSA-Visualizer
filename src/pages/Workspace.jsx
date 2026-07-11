import { useState, useMemo, useCallback, useRef, useEffect } from "react";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import TitleBar from "@/components/TitleBar";
import CodeEditor from "@/components/editor/CodeEditor";
import VisualizationCanvas from "@/components/canvas/VisualizationCanvas";
import Timeline from "@/components/canvas/Timeline";
import Sidebar from "@/components/sidebar/Sidebar";
import DebugOverlay from "@/components/debug/DebugOverlay";
import { usePlayback } from "@/lib/usePlayback";
import { useTheme } from "@/lib/useTheme";
import { useDebugMode } from "@/lib/useDebugMode";
import { runCode } from "@/lib/runCode";
import { adaptBackendTrace } from "@/lib/adaptBackendTrace";
import { diffSnapshots, diffVariables } from "@/lib/diffEngine";
import { generateExplanation } from "@/lib/explanations";
import { EXAMPLES } from "@/lib/examples";

const SKIP_TYPES = new Set(["function", "unsupported", "module", "type"]);

function createErrorSnapshot(message, type = "ExecutionError") {
  return {
    step: 0,
    line: null,
    code: "",
    function: "<module>",
    event: "exception",
    stdout: "",
    exception: {
      type,
      message: message || "Execution failed",
      line: null,
    },
    locals: [],
    globals: {},
    heap: [],
  };
}

function errorTypeLabel(errorType) {
  if (!errorType) return "ExecutionError";
  return errorType
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join("");
}

export default function Workspace() {
  const { theme, toggle } = useTheme();
  const [debugActive, setDebugActive] = useDebugMode();

  const [selectedExample, setSelectedExample] = useState("");
  const [code, setCode] = useState('print("Hello World")\n');
  const [trace, setTrace] = useState([]);
  const [demoMode, setDemoMode] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [executionTime, setExecutionTime] = useState(null);
  const [runStatus, setRunStatus] = useState("idle");
  const [runError, setRunError] = useState("");
  const abortControllerRef = useRef(null);
  const justRanLiveRef = useRef(false);

  const playback = usePlayback(trace);
  const { step } = playback;

  const currentSnapshot = trace[step];
  const prevSnapshot = step > 0 ? trace[step - 1] : null;

  const events = useMemo(
    () => diffSnapshots(prevSnapshot, currentSnapshot),
    [prevSnapshot, currentSnapshot]
  );

  const variableDiffs = useMemo(
    () => diffVariables(prevSnapshot, currentSnapshot),
    [prevSnapshot, currentSnapshot]
  );

  const explanation = useMemo(
    () => generateExplanation(currentSnapshot, prevSnapshot, events),
    [currentSnapshot, prevSnapshot, events]
  );

  const handleRun = useCallback(async () => {
    abortControllerRef.current?.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setIsRunning(true);
    setRunStatus("idle");
    setRunError("");

    try {
      const result = await runCode(code, "", {}, { signal: controller.signal });
      const adaptedTrace = adaptBackendTrace(result.trace);
      const nextTrace = adaptedTrace.length
        ? adaptedTrace
        : result.error
          ? [createErrorSnapshot(result.error, errorTypeLabel(result.error_type))]
          : [];

      if (abortControllerRef.current !== controller) return;

      justRanLiveRef.current = !result.demoMode && !result.error;
      setTrace(nextTrace);
      setDemoMode(Boolean(result.demoMode));
      setExecutionTime(typeof result.execution_time === "number" ? result.execution_time : null);
      setRunError(result.error || "");
      setRunStatus(result.error ? "error" : "success");
    } catch (error) {
      if (error?.name === "AbortError") return;
      if (abortControllerRef.current !== controller) return;

      const message = error instanceof Error ? error.message : "Failed to run code";
      setTrace([createErrorSnapshot(message, "ApiError")]);
      setDemoMode(false);
      setExecutionTime(null);
      setRunError(message);
      setRunStatus("error");
    } finally {
      if (abortControllerRef.current === controller) {
        setIsRunning(false);
        abortControllerRef.current = null;
      }
    }
  }, [code]);

  const handleStop = useCallback(() => {
    abortControllerRef.current?.abort();
  }, []);

  const handleReset = useCallback(() => {
    abortControllerRef.current?.abort();
    abortControllerRef.current = null;
    setIsRunning(false);
    setRunStatus("idle");
    setRunError("");
    setTrace([]);
    setExecutionTime(null);
    setDemoMode(false);
  }, []);

  useEffect(() => {
    if (runStatus === "idle") return;
    const t = setTimeout(() => setRunStatus("idle"), 2500);
    return () => clearTimeout(t);
  }, [runStatus]);

  useEffect(() => {
    if (!runError || !trace.length) return;
    const exceptionIdx = trace.findIndex((snap) => snap?.event === "exception");
    if (exceptionIdx > 0) playback.goToStep(exceptionIdx);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [runError, trace]);

  useEffect(() => {
    if (!justRanLiveRef.current) return;
    justRanLiveRef.current = false;
    if (!trace.length) return;
    const firstIdx = trace.findIndex(
      (snap) => (snap?.heap || []).some((obj) => !SKIP_TYPES.has(obj.type))
    );
    if (firstIdx > 0) playback.goToStep(firstIdx);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [trace]);

  const handleSelectExample = useCallback((key) => {
    const example = EXAMPLES.find((e) => e.key === key);
    if (!example) return;
    setSelectedExample(key);
    setCode(example.code);
    setTrace(example.trace);
    setDemoMode(true);
    setExecutionTime(null);
    setRunStatus("idle");
    setRunError("");
  }, []);

  return (
    <div className="h-screen flex flex-col bg-background text-foreground">
      <TitleBar
        onRun={handleRun}
        onStop={handleStop}
        onReset={handleReset}
        isRunning={isRunning}
        runStatus={runStatus}
        demoMode={demoMode}
        theme={theme}
        onToggleTheme={toggle}
        examples={EXAMPLES}
        selectedExample={selectedExample}
        onSelectExample={handleSelectExample}
      />

      <div className="flex-1 overflow-hidden">
        <PanelGroup direction="horizontal" autoSaveId="dsa-layout">
          {/* Left: Code Editor with breakpoint gutter */}
          <Panel defaultSize={25} minSize={15}>
            <CodeEditor
              value={code}
              onChange={setCode}
              theme={theme}
              breakpoints={playback.breakpoints}
              onToggleBreakpoint={playback.toggleBreakpoint}
            />
          </Panel>

          <PanelResizeHandle className="w-1 bg-border hover:bg-primary active:bg-primary transition-colors" />

          {/* Center: Visualization + Timeline */}
          <Panel defaultSize={50} minSize={30}>
            <div className="h-full flex flex-col">
              <div className="flex-1 overflow-hidden bg-canvas relative">
                <VisualizationCanvas snapshot={currentSnapshot} events={events} />
                {runError && (
                  <div className="absolute left-4 right-4 bottom-4 rounded border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive shadow-sm">
                    {runError}
                  </div>
                )}
                {debugActive && (
                  <DebugOverlay
                    snapshot={currentSnapshot}
                    events={events}
                    step={step}
                    maxStep={playback.maxStep}
                    onClose={() => setDebugActive(false)}
                  />
                )}
              </div>
              <Timeline playback={playback} trace={trace} />
            </div>
          </Panel>

          <PanelResizeHandle className="w-1 bg-border hover:bg-primary active:bg-primary transition-colors" />

          {/* Right: Sidebar with tabs */}
          <Panel defaultSize={25} minSize={15}>
            <Sidebar
              code={code}
              snapshot={currentSnapshot}
              explanation={explanation}
              stdout={currentSnapshot?.stdout}
              variableDiffs={variableDiffs}
              totalSteps={trace.length}
              executionTime={executionTime}
              demoMode={demoMode}
              trace={trace}
              step={step}
              watchedVars={playback.watchedVars}
              onAddWatch={playback.addWatch}
              onRemoveWatch={playback.removeWatch}
              breakpoints={playback.breakpoints}
              onToggleBreakpoint={playback.toggleBreakpoint}
              events={events}
              theme={theme}
            />
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
}