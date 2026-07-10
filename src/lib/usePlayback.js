import { useState, useCallback, useEffect, useRef } from "react";

export function usePlayback(trace) {
  const [step, setStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const maxStep = Math.max(0, trace.length - 1);

  // breakpoints: Set<number> (line numbers), managed externally via setBreakpoints
  const [breakpoints, setBreakpoints] = useState(new Set());
  // watchedVars: Set<string> (variable names)
  const [watchedVars, setWatchedVars] = useState(new Set());

  // Ref used by the "continue to breakpoint" interval to know the current step
  const stepRef = useRef(0);
  useEffect(() => { stepRef.current = step; }, [step]);

  const next = useCallback(() => {
    setStep((s) => Math.min(s + 1, maxStep));
  }, [maxStep]);

  const prev = useCallback(() => {
    setStep((s) => Math.max(s - 1, 0));
  }, []);

  const togglePlay = useCallback(() => {
    setStep((s) => {
      if (s >= maxStep) {
        setIsPlaying(false);
        return s;
      }
      setIsPlaying((p) => !p);
      return s;
    });
  }, [maxStep]);

  const pause = useCallback(() => setIsPlaying(false), []);

  const restart = useCallback(() => {
    setStep(0);
    setIsPlaying(false);
  }, []);

  const goToStep = useCallback(
    (n) => {
      setIsPlaying(false);
      setStep(Math.max(0, Math.min(n, maxStep)));
    },
    [maxStep]
  );

  // Step Over: advance until call_stack depth <= current depth
  const stepOver = useCallback(() => {
    setIsPlaying(false);
    setStep((s) => {
      const currentDepth = trace[s]?.locals?.length ?? 1;
      let next = s + 1;
      while (next <= maxStep) {
        const d = trace[next]?.locals?.length ?? 1;
        if (d <= currentDepth) return next;
        next++;
      }
      return maxStep;
    });
  }, [trace, maxStep]);

  // Step Out: advance until call_stack depth < current depth
  const stepOut = useCallback(() => {
    setIsPlaying(false);
    setStep((s) => {
      const currentDepth = trace[s]?.locals?.length ?? 1;
      let next = s + 1;
      while (next <= maxStep) {
        const d = trace[next]?.locals?.length ?? 1;
        if (d < currentDepth) return next;
        next++;
      }
      return maxStep;
    });
  }, [trace, maxStep]);

  // Continue: play until hitting a breakpoint line (first hit only)
  const continueToBreakpoint = useCallback(() => {
    if (!trace.length) return;
    const currentStep = stepRef.current;
    if (currentStep >= maxStep) return;

    if (breakpoints.size === 0) {
      // No breakpoints — behave like normal play
      setStep((s) => {
        if (s >= maxStep) { setIsPlaying(false); return s; }
        setIsPlaying(true);
        return s;
      });
      return;
    }

    // Instant-advance to the next breakpoint
    let target = maxStep;
    for (let i = currentStep + 1; i <= maxStep; i++) {
      if (breakpoints.has(trace[i]?.line)) {
        target = i;
        break;
      }
    }
    setStep(target);
    setIsPlaying(false);
  }, [trace, maxStep, breakpoints]);

  const toggleBreakpoint = useCallback((line) => {
    setBreakpoints((prev) => {
      const next = new Set(prev);
      if (next.has(line)) next.delete(line);
      else next.add(line);
      return next;
    });
  }, []);

  const addWatch = useCallback((name) => {
    setWatchedVars((prev) => new Set([...prev, name]));
  }, []);

  const removeWatch = useCallback((name) => {
    setWatchedVars((prev) => {
      const next = new Set(prev);
      next.delete(name);
      return next;
    });
  }, []);

  // Playback interval — respects Instant speed (speed === 0 = jump to end)
  useEffect(() => {
    if (!isPlaying) return;

    if (speed === 0) {
      // Instant: jump to end (or next breakpoint)
      if (breakpoints.size > 0) {
        const s = stepRef.current;
        let target = maxStep;
        for (let i = s + 1; i <= maxStep; i++) {
          if (breakpoints.has(trace[i]?.line)) { target = i; break; }
        }
        setStep(target);
      } else {
        setStep(maxStep);
      }
      setIsPlaying(false);
      return;
    }

    const delay = 600 / speed;
    const interval = setInterval(() => {
      setStep((s) => {
        if (s >= maxStep) {
          setIsPlaying(false);
          return s;
        }
        const next = s + 1;
        // Stop on breakpoint lines during normal play
        if (breakpoints.size > 0 && breakpoints.has(trace[next]?.line)) {
          setIsPlaying(false);
          return next;
        }
        return next;
      });
    }, delay);
    return () => clearInterval(interval);
  }, [isPlaying, speed, maxStep, breakpoints, trace]);

  useEffect(() => {
    setStep(0);
    setIsPlaying(false);
  }, [trace]);

  return {
    step,
    isPlaying,
    speed,
    next,
    prev,
    togglePlay,
    pause,
    restart,
    goToStep,
    setSpeed,
    maxStep,
    isFirst: step === 0,
    isLast: step === maxStep,
    stepOver,
    stepOut,
    continueToBreakpoint,
    breakpoints,
    toggleBreakpoint,
    watchedVars,
    addWatch,
    removeWatch,
  };
}
