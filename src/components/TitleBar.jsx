import { Play, Moon, Sun, ChevronDown, Square, RotateCcw, Loader2, CheckCircle2, XCircle } from "lucide-react";

export default function TitleBar({
  onRun,
  onStop,
  onReset,
  isRunning,
  runStatus = "idle",
  demoMode,
  theme,
  onToggleTheme,
  examples = [],
  selectedExample,
  onSelectExample,
}) {
  return (
    <div className="h-10 flex items-center justify-between px-3 bg-titlebar border-b border-border no-select shrink-0">
      {/* Left: traffic lights */}
      <div className="flex items-center gap-2 w-40">
        <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
        <div className="w-3 h-3 rounded-full bg-[#FEBC2E]" />
        <div className="w-3 h-3 rounded-full bg-[#28C840]" />
      </div>

      {/* Center: app name + example selector */}
      <div className="flex items-center gap-3 text-xs font-medium text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <img
            src="https://i.pinimg.com/736x/b9/88/1d/b9881d73712f3e4aa410348dcabcb8b3.jpg"
            alt="Visam"
            className="w-4 h-4 rounded-sm object-cover"
          />
          <span className="tracking-wide">Visam</span>
        </div>
        {examples.length > 0 && (
          <div className="relative flex items-center">
            <select
              value={selectedExample}
              onChange={(e) => onSelectExample(e.target.value)}
              className="appearance-none bg-transparent text-xs text-muted-foreground pr-5 pl-2 cursor-pointer outline-none border-l border-border"
            >
              <option value="" disabled>Examples</option>
              {examples.map((ex) => (
                <option key={ex.key} value={ex.key}>
                  {ex.label}
                </option>
              ))}
            </select>
            <ChevronDown className="w-3 h-3 absolute right-0 pointer-events-none text-muted-foreground" />
          </div>
        )}
      </div>

      {/* Right: actions */}
      <div className="flex items-center gap-2 w-auto justify-end">
        {demoMode && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-muted text-muted-foreground">
            Demo mode
          </span>
        )}
        {!isRunning && runStatus === "success" && (
          <span className="flex items-center gap-1 text-[10px] font-medium text-emerald-500">
            <CheckCircle2 className="w-3 h-3" /> Finished
          </span>
        )}
        {!isRunning && runStatus === "error" && (
          <span className="flex items-center gap-1 text-[10px] font-medium text-destructive">
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
            className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-destructive text-destructive-foreground text-xs font-medium hover:opacity-90 transition-opacity"
          >
            <Square className="w-3 h-3 fill-current" />
            Stop
          </button>
        ) : (
          <button
            onClick={onRun}
            className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-primary text-primary-foreground text-xs font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
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