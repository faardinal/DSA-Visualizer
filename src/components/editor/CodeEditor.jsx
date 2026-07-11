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
  const observerRef = useRef(null);
  const decorationsRef = useRef([]);

  const handleMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    defineThemes(monaco);
    monaco.editor.setTheme(themeName(theme));

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
    monaco.editor.setTheme(themeName(theme));
  }, [theme]);

  return (
    <div className="h-full w-full bg-sidebar">
      <Editor
        value={value}
        language="python"
        theme={themeName(theme)}
        onMount={handleMount}
        onChange={(val) => onChange(val ?? "")}
        options={BASE_EDITOR_OPTIONS}
      />
    </div>
  );
}