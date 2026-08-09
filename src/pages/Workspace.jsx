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
import { runSolution } from "@/lib/runSolution";
import { adaptBackendTrace } from "@/lib/adaptBackendTrace";
import { adaptSolutionResult } from "@/lib/adaptSolutionTrace";
import { diffSnapshots, diffVariables } from "@/lib/diffEngine";
import { generateExplanation } from "@/lib/explanations";
import { EXAMPLES } from "@/lib/examples";
import TestResultsPanel from "@/components/TestResultsPanel";
import ProblemSelector from "@/components/ProblemSelector";

const SKIP_TYPES = new Set(["function", "unsupported", "module", "type"]);

// Detect LeetCode mode: code contains a Solution class definition
function isLeetCodeCode(code) {
  return /class\s+Solution\s*[:\(]/.test(code);
}

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

  // LeetCode mode state
  const [leetCodeMode, setLeetCodeMode] = useState(false);
  const [testResults, setTestResults] = useState([]);
  const [solutionStats, setSolutionStats] = useState(null);
  const [problemId, setProblemId] = useState(null);
  const [problemTitle, setProblemTitle] = useState(null);
  const [ambiguousProblems, setAmbiguousProblems] = useState(null);
  const [replayTestIdx, setReplayTestIdx] = useState(null);
  const [solutionSessionId, setSolutionSessionId] = useState(null);
  const [solutionVerdict, setSolutionVerdict] = useState(null);

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

    const useLeetCode = isLeetCodeCode(code);
    setLeetCodeMode(useLeetCode);

    try {
      if (useLeetCode) {
        const result = await runSolution(
          code,
          { problemId: problemId || undefined, replayTestIdx, sessionId: solutionSessionId || undefined, mode: "submit" },
          { signal: controller.signal }
        );
        if (abortControllerRef.current !== controller) return;

        const adapted = adaptSolutionResult(result);

        // Ambiguity: multiple problems match the method name
        if (adapted.ambiguousProblems && adapted.ambiguousProblems.length > 0) {
          setAmbiguousProblems(adapted.ambiguousProblems);
          setRunError(adapted.error || "Multiple problems match. Please select one.");
          setRunStatus("error");
          setTrace([]);
          setTestResults([]);
          setSolutionStats(null);
        } else if (adapted.error && !adapted.trace.length) {
          setTrace([createErrorSnapshot(adapted.error, errorTypeLabel(adapted.errorType))]);
          setTestResults([]);
          setSolutionStats(null);
          setRunError(adapted.error);
          setRunStatus("error");
        } else {
          justRanLiveRef.current = true;
          setTrace(adapted.trace.length ? adapted.trace : (adapted.error ? [createErrorSnapshot(adapted.error, errorTypeLabel(adapted.errorType))] : []));
          setTestResults(adapted.testResults);
          setSolutionStats(adapted.statistics);
          setProblemTitle(adapted.problemTitle);
          setSolutionSessionId(adapted.sessionId);
          setSolutionVerdict(adapted.status);
          setAmbiguousProblems(null);
          setExecutionTime(adapted.executionTime);
          setRunError(adapted.error || "");
          setRunStatus(adapted.passed ? "success" : (adapted.error ? "error" : "success"));
        }
      } else {
        // Free-form mode (existing behavior)
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
        setTestResults([]);
        setSolutionStats(null);
        setExecutionTime(typeof result.execution_time === "number" ? result.execution_time : null);
        setRunError(result.error || "");
        setRunStatus(result.error ? "error" : "success");
      }
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
  }, [code, problemId, replayTestIdx]);

  // Replay a specific failed test case for visualization
  const handleReplayTest = useCallback((testIdx) => {
    setReplayTestIdx(testIdx);
    // Trigger re-run with this test index
    setTimeout(() => handleRun(), 0);
  }, [handleRun]);

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
    setLeetCodeMode(false);
    setTestResults([]);
    setSolutionStats(null);
    setProblemId(null);
    setProblemTitle(null);
    setAmbiguousProblems(null);
    setReplayTestIdx(null);
    setSolutionSessionId(null);
    setSolutionVerdict(null);
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

  const handleSelectProblem = useCallback((pid, starterCode) => {
    // Set the active problem id so the backend knows which tests to run
    setProblemId(pid);
    // Load the canonical starter code into the editor
    if (starterCode) setCode(starterCode);
    // Clear ALL stale execution/trace/result/session state
    setSolutionSessionId(null);
    setReplayTestIdx(null);
    setSolutionVerdict(null);
    setAmbiguousProblems(null);
    setTestResults([]);
    setSolutionStats(null);
    setTrace([]);
    setRunStatus('idle');
    setRunError('');
    // Reset these too so the UI reflects a clean slate
    setExecutionTime(null);
    setLeetCodeMode(false);
    setProblemTitle(null);
    setDemoMode(false);
  }, []);

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
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-background text-foreground">
      <TitleBar
        onRun={handleRun}
        onStop={handleStop}
        onReset={handleReset}
        isRunning={isRunning}
        runStatus={runStatus}
        demoMode={demoMode}
        leetCodeMode={leetCodeMode}
        problemTitle={problemTitle}
        theme={theme}
        onToggleTheme={toggle}
        examples={EXAMPLES}
        selectedExample={selectedExample}
        onSelectExample={handleSelectExample}
        selectedProblemId={problemId}
        onSelectProblem={handleSelectProblem}
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

          <PanelResizeHandle className="w-px bg-border hover:bg-muted-foreground/20 active:bg-muted-foreground/30 transition-colors cursor-col-resize" />

          {/* Center: Visualization + Timeline + (LeetCode) Test Results */}
          <Panel defaultSize={50} minSize={30}>
            <div className="h-full flex flex-col">
              {/* LeetCode mode: problem selector + ambiguous prompt */}
              {leetCodeMode && (
                <div className="flex items-center gap-2 px-3 py-1.5 border-b border-border bg-sidebar/50 shrink-0">
                  <ProblemSelector
                    selectedId={problemId}
                    onSelect={(pid, starterCode) => {
                      setProblemId(pid);
                      if (starterCode) setCode(starterCode);
                      setAmbiguousProblems(null);
                      setSolutionSessionId(null);
                      setReplayTestIdx(null);
                      setSolutionVerdict(null);
                    }}
                  />
                  {problemTitle && (
                    <span className="text-[11px] text-muted-foreground truncate">{problemTitle}</span>
                  )}
                  {solutionVerdict && (
                    <span className={`text-[10px] font-semibold ${solutionVerdict === "ACCEPTED" ? "text-emerald-500" : "text-destructive"}`}>
                      {solutionVerdict.replaceAll("_", " ")}
                    </span>
                  )}
                </div>
              )}
              <div className="flex-1 overflow-hidden bg-canvas relative">
                <VisualizationCanvas snapshot={currentSnapshot} events={events} />
                {runError && !ambiguousProblems && (
                  <div className="absolute left-4 right-4 bottom-4 rounded border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive shadow-sm">
                    {runError}
                  </div>
                )}
                {ambiguousProblems && (
                  <div className="absolute left-4 right-4 bottom-4 rounded border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-600 dark:text-amber-400 shadow-sm">
                    Multiple problems match. Select one above.
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
              {/* LeetCode mode: test results panel above timeline */}
              {leetCodeMode && testResults.length > 0 && (
                <div className="h-48 border-t border-border shrink-0">
                  <TestResultsPanel
                    testResults={testResults}
                    statistics={solutionStats}
                    onReplayTest={handleReplayTest}
                    replayTestIdx={replayTestIdx}
                  />
                </div>
              )}
              <Timeline playback={playback} trace={trace} />
            </div>
          </Panel>

          <PanelResizeHandle className="w-px bg-border hover:bg-muted-foreground/20 active:bg-muted-foreground/30 transition-colors cursor-col-resize" />

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
