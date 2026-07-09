import {
  SkipBack, Play, Pause, SkipForward, RotateCcw, ChevronFirst, ChevronLast,
  StepForward, FastForward, Square
} from "lucide-react";
import { useEffect, useMemo } from "react";

const SPEEDS = [0.25, 0.5, 1, 2, 4, 0]; // 0 = Instant
const SPEED_LABELS = { 0.25: "0.25x", 0.5: "0.5x", 1: "1x", 2: "2x", 4: "4x", 0: "⚡" };

export default function Timeline({ playback, trace }) {
  const {
    step, maxStep, isPlaying, speed,
    next, prev, togglePlay, restart, goToStep, setSpeed,
    isFirst, isLast,
    stepOver, stepOut, continueToBreakpoint, breakpoints,
  } = playback;

  const framePreview = useMemo(() => {
    if (!trace || !trace[step]) return "";
    const snap = trace[step];
    const code = snap.code?.trim() || "";
    return code.length > 60 ? code.substring(0, 57) + "…" : code;
  }, [trace, step]);

  const eventBadge = useMemo(() => {
    const snap = trace?.[step];
    if (!snap) return null;
    if (snap.event === "exception") return { label: "EXCEPTION", cls: "text-destructive" };
    if (snap.event === "return") return { label: "RETURN", cls: "text-primary" };
    const prevDepth = trace?.[step - 1]?.locals?.length ?? 1;
    const currDepth = snap.locals?.length ?? 1;
    if (snap.event === "line" && currDepth > prevDepth) return { label: "CALL", cls: "text-primary" };
    return null;
  }, [trace, step]);

  // Compute timeline markers once for all steps
  const markers = useMemo(() => {
    if (!trace || trace.length === 0) return [];
    const out = [];
    for (let i = 0; i < trace.length; i++) {
      const snap = trace[i];
      const prevDepth = i > 0 ? (trace[i - 1]?.locals?.length ?? 1) : 1;
      const currDepth = snap.locals?.length ?? 1;
      const prevHeapSize = i > 0 ? (trace[i - 1]?.heap?.length ?? 0) : 0;
      const currHeapSize = snap.heap?.length ?? 0;

      if (snap.event === "exception") {
        out.push({ step: i, kind: "exception", symbol: "■", color: "text-destructive" });
      } else if (snap.event === "return") {
        out.push({ step: i, kind: "return", symbol: "▲", color: "text-primary" });
      } else if (currDepth > prevDepth) {
        out.push({ step: i, kind: "call", symbol: "●", color: "text-primary" });
      } else if (currHeapSize > prevHeapSize) {
        out.push({ step: i, kind: "object_created", symbol: "★", color: "text-yellow-500" });
      }
    }
    return out;
  }, [trace]);

  // Keyboard shortcuts
  useEffect(() => {
    const hasTrace = trace && trace.length > 0;
    const handler = (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      // Monaco editor targets
      if (e.target.closest?.(".monaco-editor")) return;

      switch (e.key) {
        case " ":
          e.preventDefault();
          togglePlay();
          break;
        case "ArrowRight":
          e.preventDefault();
          next();
          break;
        case "ArrowLeft":
          e.preventDefault();
          prev();
          break;
        case "Home":
          e.preventDefault();
          goToStep(0);
          break;
        case "End":
          e.preventDefault();
          goToStep(maxStep);
          break;
        case "r":
        case "R":
          if (!e.ctrlKey && !e.metaKey) {
            e.preventDefault();
            restart();
          }
          break;
        case "1": setSpeed(0.5); break;
        case "2": setSpeed(1); break;
        case "3": setSpeed(2); break;
        // F5 = Run/Continue to breakpoint
        case "F5":
          if (hasTrace) { e.preventDefault(); continueToBreakpoint(); }
          break;
        // F10 = Step Over
        case "F10":
          if (hasTrace) { e.preventDefault(); stepOver(); }
          break;
        // F11 = Step Into (= next)
        case "F11":
          if (hasTrace) {
            e.preventDefault();
            if (e.shiftKey) stepOut();  // Shift+F11 = Step Out
            else next();
          }
          break;
        default:
          break;
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [togglePlay, next, prev, goToStep, restart, setSpeed, maxStep, stepOver, stepOut, continueToBreakpoint, trace]);

  return (
    <div className="flex flex-col bg-sidebar border-t border-border shrink-0">
      {/* Frame preview */}
      {framePreview && (
        <div className="px-4 pt-1.5 pb-0.5 flex items-center gap-2">
          {eventBadge && (
            <span className={`text-[9px] font-mono font-semibold tracking-wider shrink-0 ${eventBadge.cls}`}>
              {eventBadge.label}
            </span>
          )}
          <p className="text-[10px] font-mono text-muted-foreground/70 truncate">
            {framePreview}
          </p>
        </div>
      )}

      {/* Step counter + scrubber with markers */}
      <div className="px-4 pt-1 pb-0">
        <div className="relative flex items-center gap-3">
          <span className="text-[11px] font-mono text-muted-foreground whitespace-nowrap min-w-[60px]">
            {step + 1} / {maxStep + 1}
          </span>
          <div className="flex-1 relative h-4 flex items-center">
            {/* Marker glyphs on the scrubber track */}
            {maxStep > 0 && markers.map((m, idx) => {
              const pct = (m.step / maxStep) * 100;
              return (
                <button
                  key={idx}
                  title={`${m.kind} at step ${m.step + 1}`}
                  onClick={() => goToStep(m.step)}
                  style={{ left: `${pct}%`, transform: "translateX(-50%)" }}
                  className={`absolute text-[7px] leading-none z-10 ${m.color} hover:scale-150 transition-transform`}
                >
                  {m.symbol}
                </button>
              );
            })}
            <input
              type="range"
              min={0}
              max={maxStep}
              value={step}
              onChange={(e) => goToStep(Number(e.target.value))}
              className="w-full h-1 accent-primary cursor-pointer relative z-20"
              aria-label="Step slider"
              style={{ opacity: 0.9 }}
            />
          </div>
        </div>
      </div>

      {/* Controls row */}
      <div className="h-12 flex items-center justify-between px-4">
        {/* Transport + step controls */}
        <div className="flex items-center gap-0.5">
          <IconButton onClick={() => goToStep(0)} disabled={isFirst} title="First (Home)">
            <ChevronFirst className="w-4 h-4" />
          </IconButton>
          <IconButton onClick={prev} disabled={isFirst} title="Previous (←)">
            <SkipBack className="w-4 h-4" />
          </IconButton>
          <button
            onClick={togglePlay}
            disabled={isLast && !isPlaying}
            className="w-9 h-9 flex items-center justify-center rounded-lg bg-primary text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-40"
            title={isPlaying ? "Pause (Space)" : "Play (Space)"}
          >
            {isPlaying ? <Pause className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current" />}
          </button>
          <IconButton onClick={next} disabled={isLast} title="Next / Step Into (→ or F11)">
            <SkipForward className="w-4 h-4" />
          </IconButton>
          <IconButton onClick={() => goToStep(maxStep)} disabled={isLast} title="Last (End)">
            <ChevronLast className="w-4 h-4" />
          </IconButton>
          <IconButton onClick={restart} title="Restart (R)">
            <RotateCcw className="w-3.5 h-3.5" />
          </IconButton>

          {/* Divider */}
          <div className="w-px h-5 bg-border mx-0.5" />

          {/* Step Over */}
          <IconButton
            onClick={stepOver}
            disabled={isLast}
            title="Step Over (F10)"
            className="text-[10px] font-mono"
          >
            <span className="text-[10px] font-bold leading-none select-none">↷</span>
          </IconButton>

          {/* Step Out */}
          <IconButton
            onClick={stepOut}
            disabled={isLast}
            title="Step Out (Shift+F11)"
            className="text-[10px] font-mono"
          >
            <span className="text-[10px] font-bold leading-none select-none">↑↑</span>
          </IconButton>

          {/* Continue to breakpoint */}
          <IconButton
            onClick={continueToBreakpoint}
            disabled={isLast}
            title={`Continue${(breakpoints?.size || 0) > 0 ? " to next breakpoint" : " (play)"} (F5)`}
          >
            <FastForward className="w-3.5 h-3.5" />
          </IconButton>
        </div>

        {/* Speed controls */}
        <div className="flex items-center gap-0.5">
          {SPEEDS.map((s) => (
            <button
              key={s}
              onClick={() => setSpeed(s)}
              className={`px-1.5 py-1 rounded-md text-[10px] font-mono transition-colors ${
                speed === s ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-muted"
              }`}
              title={s === 0 ? "Instant (jump to end/breakpoint)" : `${s}x speed`}
            >
              {SPEED_LABELS[s]}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function IconButton({ children, className = "", ...props }) {
  return (
    <button
      {...props}
      className={`w-8 h-8 flex items-center justify-center rounded-md text-muted-foreground hover:bg-muted disabled:opacity-30 disabled:hover:bg-transparent transition-colors ${className}`}
    >
      {children}
    </button>
  );
}
