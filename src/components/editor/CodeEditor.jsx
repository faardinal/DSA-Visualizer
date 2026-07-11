
import Editor from "@monaco-editor/react";
import { useRef, useEffect } from "react";
import { defineThemes, themeName, BASE_EDITOR_OPTIONS } from "@/lib/monacoTheme";

// Editable left-panel Monaco editor. Theme + breakpoint decorations are
// shared with the read-only CODE viewer via lib/monacoTheme.js and the
// global CSS classes in index.css (bp-line-highlight / bp-glyph /
// dsa-active-line / dsa-active-glyph).

export default function CodeEditor({ value, onChange, theme, breakpoints, onToggleBreakpoint }) {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
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
    defineThemes(monaco);
    monaco.editor.setTheme(themeName(theme));

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
    editor.layout();
  };

  const handleUnmount = () => {
    observerRef.current?.disconnect();
    observerRef.current = null;
  };

  // Apply breakpoint decorations whenever breakpoints set changes
  useEffect(() => {
    const editor = editorRef.current;
  useEffect(() => {
    const monaco = monacoRef.current;
    if (!monaco) return;
    monaco.editor.setTheme(theme === "dark" ? "dsa-dark" : "dsa-light");
    monaco.editor.setTheme(themeName(theme));
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
        theme={themeName(theme)}
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
        options={BASE_EDITOR_OPTIONS}
      />
    </div>
  );
