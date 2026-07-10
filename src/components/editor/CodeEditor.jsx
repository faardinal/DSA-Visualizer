import Editor from "@monaco-editor/react";
import { useRef, useEffect } from "react";

export default function CodeEditor({ value, onChange, theme, breakpoints, onToggleBreakpoint }) {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const observerRef = useRef(null);
  const decorationsRef = useRef([]);

  const handleMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    monaco.editor.defineTheme("dsa-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [],
      colors: {
        "editor.background": "#161618",
        "editor.foreground": "#EBEBEB",
        "editorLineNumber.foreground": "#5A5A5E",
        "editorLineNumber.activeForeground": "#EBEBEB",
        "editor.lineHighlightBackground": "#FFFFFF08",
        "editorCursor.foreground": "#007AFF",
        "editor.selectionBackground": "#007AFF33",
        "editorIndentGuide.background": "#2A2A2C",
        "editorIndentGuide.activeBackground": "#3A3A3C",
        "editorGutter.background": "#161618",
      },
    });

    monaco.editor.defineTheme("dsa-light", {
      base: "vs",
      inherit: true,
      rules: [],
      colors: {
        "editor.background": "#EDEDEF",
        "editor.foreground": "#1D1D1F",
        "editorLineNumber.foreground": "#AEAEB2",
        "editorLineNumber.activeForeground": "#1D1D1F",
        "editor.lineHighlightBackground": "#00000006",
        "editorCursor.foreground": "#007AFF",
        "editor.selectionBackground": "#007AFF33",
        "editorIndentGuide.background": "#D5D5DA",
        "editorGutter.background": "#EDEDEF",
      },
    });

    monaco.editor.setTheme(theme === "dark" ? "dsa-dark" : "dsa-light");

    // Gutter click → toggle breakpoint
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

    const domNode = editor.getDomNode();
    if (domNode) {
      observerRef.current = new ResizeObserver(() => {
        editor.layout();
      });
      observerRef.current.observe(domNode.parentElement || domNode);
    }

    editor.layout();
  };

  const handleUnmount = () => {
    observerRef.current?.disconnect();
    observerRef.current = null;
  };

  // Apply breakpoint decorations whenever breakpoints set changes
  useEffect(() => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    if (!editor || !monaco) return;

    const bpArray = breakpoints ? Array.from(breakpoints) : [];
    const newDecorations = bpArray.map((line) => ({
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
    }));

    decorationsRef.current = editor.deltaDecorations(decorationsRef.current, newDecorations);
  }, [breakpoints]);

  // Update theme when prop changes
  useEffect(() => {
    const monaco = monacoRef.current;
    if (!monaco) return;
    monaco.editor.setTheme(theme === "dark" ? "dsa-dark" : "dsa-light");
  }, [theme]);

  return (
    <div className="h-full w-full bg-sidebar">
      <style>{`
        .bp-line-highlight { background: rgba(239,68,68,0.12) !important; }
        .bp-glyph {
          background: radial-gradient(circle at 50% 50%, #ef4444 55%, transparent 56%);
          width: 10px !important;
          margin-left: 3px;
        }
      `}</style>
      <Editor
        value={value}
        language="python"
        theme={theme === "dark" ? "dsa-dark" : "dsa-light"}
        onMount={handleMount}
        onChange={(val) => onChange(val ?? "")}
        options={{
          fontFamily: "SF Mono, ui-monospace, Menlo, monospace",
          fontSize: 13,
          lineHeight: 20,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          padding: { top: 12 },
          renderLineHighlight: "line",
          overviewRulerLanes: 1,
          hideCursorInOverviewRuler: false,
          overviewRulerBorder: false,
          glyphMargin: true,
          scrollbar: {
            verticalScrollbarSize: 4,
            horizontalScrollbarSize: 4,
          },
          fontLigatures: true,
        }}
      />
    </div>
  );
}
