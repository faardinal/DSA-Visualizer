import {
  Play, Moon, Sun, ChevronDown, Square, RotateCcw,
  Loader2, CheckCircle2, XCircle,
} from "lucide-react";
import ProblemSelector from "@/components/ProblemSelector";

export default function TitleBar({
  onRun,
  onStop,
  onReset,
  isRunning,
  runStatus = "idle",
  demoMode,
  leetCodeMode,
  problemTitle,
  theme,
  onToggleTheme,
  examples = [],
  selectedExample,
  onSelectExample,
  // Problem picker
  selectedProblemId,
  onSelectProblem,
}) {
  return (
    <div
      className="h-10 flex items-center justify-between px-3 border-b border-border no-select shrink-0"
      style={{ background: "hsl(var(--titlebar))" }}
    >
      {/* Left: traffic lights */}
      <div className="flex items-center gap-2" style={{ minWidth: 80 }}>
        <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
        <div className="w-3 h-3 rounded-full bg-[#FEBC2E]" />
        <div className="w-3 h-3 rounded-full bg-[#28C840]" />
      </div>

      {/* Center: app name · example selector · problem picker */}
      <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground flex-1 justify-center overflow-hidden">
        {/* App name */}
        <div className="flex items-center gap-1.5 shrink-0">
          <img
            src="https://i.pinimg.com/736x/b9/88/1d/b9881d73712f3e4aa410348dcabcb8b3.jpg"
            alt="Visam"
            className="w-4 h-4 rounded-sm object-cover"
          />
          <span className="tracking-wide">Visam</span>
        </div>

        {/* Examples dropdown */}
        {examples.length > 0 && (
          <div className="relative flex items-center shrink-0">
            <select
              value={selectedExample}
              onChange={(e) => onSelectExample(e.target.value)}
              className="appearance-none bg-transparent text-xs text-muted-foreground pr-5 pl-2 cursor-pointer outline-none border-l border-border"
            >
              <option value="" disabled>Examples</option>
              {examples.map((ex) => (
                <option key={ex.key} value={ex.key}>{ex.label}</option>
              ))}
            </select>
            <ChevronDown className="w-3 h-3 absolute right-0 pointer-events-none text-muted-foreground" />
          </div>
        )}

        {/* Problem picker — always visible, compact */}
        <ProblemSelector
          selectedId={selectedProblemId}
          onSelect={onSelectProblem}
        />
      </div>

      {/* Right: status indicators + actions */}
      <div className="flex items-center gap-2 justify-end" style={{ minWidth: 140 }}>
        {demoMode && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-muted text-muted-foreground shrink-0">
            Demo mode
          </span>
        )}
        {leetCodeMode && !selectedProblemId && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-primary/15 text-primary shrink-0">
            LeetCode{problemTitle ? ` · ${problemTitle}` : ""}
          </span>
        )}
        {!isRunning && runStatus === "success" && (
          <span className="flex items-center gap-1 text-[10px] font-medium text-emerald-500 shrink-0">
            <CheckCircle2 className="w-3 h-3" /> Finished
          </span>
        )}
        {!isRunning && runStatus === "error" && (
          <span className="flex items-center gap-1 text-[10px] font-medium text-destructive shrink-0">
            <XCircle className="w-3 h-3" /> Failed
          </span>
        )}

        <button
          onClick={onToggleTheme}
          className="p-1.5 rounded-md hover:bg-muted text-muted-foreground transition-colors"
          aria-label="Toggle theme"
        >
          {theme === "dark" ? <Sun className="w-3.5 h-3.5" /> : <Moon className="w-3.5 h-3.5" />}
        </button>

        <button
          onClick={onReset}
          disabled={isRunning}
          className="p-1.5 rounded-md hover:bg-muted text-muted-foreground transition-colors disabled:opacity-40"
          aria-label="Reset workspace"
          title="Reset"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>

        {isRunning ? (
          <button
            onClick={onStop}
            className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-destructive text-destructive-foreground text-xs font-medium hover:opacity-90 transition-opacity shrink-0"
          >
            <Square className="w-3 h-3 fill-current" />
            Stop
          </button>
        ) : (
          <button
            onClick={onRun}
            className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-primary text-primary-foreground text-xs font-medium hover:opacity-90 transition-opacity disabled:opacity-50 shrink-0"
          >
            <Play className="w-3 h-3 fill-current" />
            Run
          </button>
        )}

        {isRunning && (
          <Loader2 className="w-3.5 h-3.5 animate-spin text-muted-foreground" aria-label="Running" />
        )}
      </div>
    </div>
  );
}
