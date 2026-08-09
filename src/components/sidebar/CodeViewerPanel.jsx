import Editor from "@monaco-editor/react";
import { useRef, useEffect, useMemo, useCallback } from "react";
import { defineThemes, themeName, BASE_EDITOR_OPTIONS } from "@/lib/monacoTheme";

// CODE tab — a read-only Monaco viewer that mirrors the program's execution.
//
// Synchronization model:
//   The ONLY source of truth for playback is `usePlayback()` in Workspace.
//   Every frame, Workspace passes the current `snapshot` (= trace[step]) to
//   this panel. We never store playback state here — we only ever read it.
//   So visualization, timeline, variables, and this viewer can never drift
//   apart, because they all derive from that single snapshot.
//
// Performance model:
//   The Monaco editor instance is created once. On each step we ONLY call
//   `deltaDecorations` (cheap) to repaint the active-line highlight and, if
//   the line is off-screen, `revealLineInCenterSmooth`. We never recreate
//   the editor, never re-set its value, never re-tokenize.

const ACTIVE_DECORATION_KEY = "dsa-active-line";

function eventBadge(event) {
  if (!event) return null;
  if (event === "exception") return { label: "EXCEPTION", cls: "text-destructive bg-destructive/10" };
  if (event === "return") return { label: "RETURN", cls: "text-primary bg-primary/10" };
  if (event === "call") return { label: "CALL", cls: "text-primary bg-primary/10" };
  if (event === "line") return { label: "LINE", cls: "text-muted-foreground bg-muted" };
  return { label: event.toUpperCase(), cls: "text-muted-foreground bg-muted" };
}

export default function CodeViewerPanel({
  code,
  snapshot,
  theme,
  breakpoints,
  onToggleBreakpoint,
}) {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const decorationsRef = useRef([]);
  const lastScrolledLineRef = useRef(null);
  const observerRef = useRef(null);

  const currentLine = snapshot?.line ?? null;
  const isException = snapshot?.event === "exception";
  const activeBadge = eventBadge(snapshot?.event);

  const lineCount = useMemo(() => (code ? code.split("\n").length : 0), [code]);

  const handleMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    defineThemes(monaco);
    monaco.editor.setTheme(themeName(theme));

    // Gutter click → toggle breakpoint (same UX as the left editor).
    editor.onMouseDown((e) => {
      const { target } = e;
      if (
        target.type === monaco.editor.MouseTargetType.GUTTER_LINE_NUMBERS ||
        target.type === monaco.editor.MouseTargetType.GUTTER_GLYPH_MARGIN
      ) {
        const line = target.position?.lineNumber;
        if (line != null && onToggleBreakpoint) {
          onToggleBreakpoint(line);
        }
      }
    });

    // Keep the editor sized to its container (the sidebar panel).
    const domNode = editor.getDomNode();
    if (domNode) {
      observerRef.current = new ResizeObserver(() => editor.layout());
      observerRef.current.observe(domNode.parentElement || domNode);
    }
    editor.layout();
  }, [onToggleBreakpoint, theme]);

  // Update theme when the app theme flips.
  useEffect(() => {
    const monaco = monacoRef.current;
    if (!monaco) return;
    monaco.editor.setTheme(themeName(theme));
  }, [theme]);

  // Repaint decorations (active line + breakpoints) whenever either changes.
  // This is the hot path during playback — keep it allocation-light.
  useEffect(() => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    if (!editor || !monaco) return;

    const decorations = [];

    // Breakpoints first (lower z visually; the active line draws over them).
    const bpArray = breakpoints ? Array.from(breakpoints) : [];
    for (const line of bpArray) {
      decorations.push({
        range: new monaco.Range(line, 1, line, 1),
        options: {
          isWholeLine: true,
          className: "bp-line-highlight",
          glyphMarginClassName: "bp-glyph",
          overviewRuler: {
            color: "rgba(239,68,68,0.8)",
            position: monaco.editor.OverviewRulerLane.Left,
          },
        },
      });
    }

    // Active line highlight (exactly one). Recolor to red on exception lines.
    if (currentLine && currentLine >= 1 && currentLine <= lineCount) {
      decorations.push({
        range: new monaco.Range(currentLine, 1, currentLine, 1),
        options: {
          isWholeLine: true,
          className: isException ? "dsa-active-line-exception" : "dsa-active-line",
          glyphMarginClassName: isException ? "dsa-active-glyph-exception" : "dsa-active-glyph",
          stickiness: monaco.editor.TrackedRangeStickiness.NeverGrowsWhenTypingAtEdges,
        },
      });
    }

    decorationsRef.current = editor.deltaDecorations(decorationsRef.current, decorations);
  }, [currentLine, isException, breakpoints, lineCount]);

  // Auto-scroll: when the active line moves out of the visible viewport,
  // smoothly re-center it. Never jump. We avoid re-scrolling to the SAME
  // line (e.g. paused on one line while inspecting variables) so the user's
  // manual scroll position is respected until playback advances.
  useEffect(() => {
    const editor = editorRef.current;
    if (!editor || !currentLine || currentLine < 1 || currentLine > lineCount) return;
    if (lastScrolledLineRef.current === currentLine) return;
    lastScrolledLineRef.current = currentLine;

    const visibleRanges = editor.getVisibleRanges();
    const visible = visibleRanges && visibleRanges.length > 0 ? visibleRanges[0] : null;
    const inView =
      visible && currentLine >= visible.startLineNumber && currentLine <= visible.endLineNumber;

    if (!inView) {
      // Smooth, centered reveal — matches VS Code's "revealLineInCenterSmooth".
      editor.revealLineInCenterSmooth(currentLine);
    }
  }, [currentLine, lineCount]);

  // Reset the "last scrolled" memory when the program is reset/changed so
  // the first frame of a new run still scrolls into view.
  useEffect(() => {
    lastScrolledLineRef.current = null;
  }, [code]);

  useEffect(() => () => observerRef.current?.disconnect(), []);

  return (
    <div className="h-full flex flex-col">
      {/* Current execution info — compact dark header */}
      <div
        className="px-3 py-2 border-b border-border shrink-0"
        style={{ background: "hsl(var(--sidebar-background))" }}
      >
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <span
            className="font-semibold uppercase tracking-wider"
            style={{ fontSize: "9px", color: "#4A4A4A" }}
          >
            Execution
          </span>
          {activeBadge && (
            <span
              className={`font-mono font-bold tracking-wider px-1.5 py-0.5 rounded ${activeBadge.cls}`}
              style={{ fontSize: "8px" }}
            >
              {activeBadge.label}
            </span>
          )}
        </div>
        <div
          className="grid gap-x-3 gap-y-0.5 font-mono"
          style={{ gridTemplateColumns: "auto 1fr", fontSize: "11px" }}
        >
          <span style={{ color: "#4A4A4A" }}>Function</span>
          <span
            className="truncate"
            style={{ color: "#E8E8E8" }}
            title={snapshot?.function ?? "—"}
          >
            {snapshot?.function ?? "—"}
          </span>
          <span style={{ color: "#4A4A4A" }}>Line</span>
          <span
            style={{
              color: isException ? "hsl(var(--destructive))" : "#E8E8E8",
              fontWeight: isException ? 600 : 400,
            }}
          >
            {currentLine ?? "—"}
          </span>
          <span style={{ color: "#4A4A4A" }}>Event</span>
          <span style={{ color: "#E8E8E8" }}>{snapshot?.event ?? "—"}</span>
        </div>
      </div>

      {/* Read-only Monaco viewer */}
      <div className="flex-1 min-h-0" style={{ background: "hsl(var(--canvas))" }}>
        <Editor
          value={code ?? ""}
          language="python"
          theme={themeName(theme)}
          onMount={handleMount}
          options={{
            ...BASE_EDITOR_OPTIONS,
            readOnly: true,
            domReadOnly: true,
            cursorBlinking: "phase",
            contextmenu: false,
            renderLineHighlight: "all",
          }}
        />
      </div>
    </div>
  );
}