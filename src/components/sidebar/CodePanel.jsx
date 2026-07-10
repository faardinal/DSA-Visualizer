import { useRef, useEffect } from "react";

export default function CodePanel({ code, currentLine, isException }) {
  const containerRef = useRef(null);
  const lines = code.split("\n");

  useEffect(() => {
    if (!currentLine || !containerRef.current) return;
    const activeEl = containerRef.current.querySelector(`[data-line="${currentLine}"]`);
    if (activeEl) {
      // Smooth scroll — center the active line, never jump abruptly
      const container = containerRef.current;
      const containerHeight = container.clientHeight;
      const elTop = activeEl.offsetTop;
      const elHeight = activeEl.offsetHeight;
      const targetScroll = elTop - containerHeight / 2 + elHeight / 2;

      container.scrollTo({
        top: Math.max(0, targetScroll),
        behavior: "smooth",
      });
    }
  }, [currentLine]);

  return (
    <div ref={containerRef} className="font-mono text-xs leading-5">
      {lines.map((line, i) => {
        const lineNum = i + 1;
        const isActive = lineNum === currentLine;
        const isErrorLine = isActive && isException;
        return (
          <div
            key={i}
            data-line={lineNum}
            className={`flex ${isErrorLine ? "bg-destructive/10" : isActive ? "bg-primary/10" : ""}`}
          >
            <span
              className={`w-8 text-right pr-2 select-none shrink-0 ${
                isErrorLine ? "text-destructive" : isActive ? "text-primary" : "text-muted-foreground/60"
              }`}
            >
              {lineNum}
            </span>
            <span
              className={`flex-1 pl-2 whitespace-pre ${
                isErrorLine
                  ? "text-destructive border-l-2 border-destructive -ml-0.5 pl-[7px]"
                  : isActive
                  ? "text-foreground border-l-2 border-primary -ml-0.5 pl-[7px]"
                  : "text-muted-foreground"
              }`}
            >
              {line || " "}
            </span>
          </div>
        );
      })}
    </div>
  );
}