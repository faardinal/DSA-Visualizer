/**
 * monacoTheme.js
 * Monaco editor theme definitions and shared editor options.
 * Used by both the editable CodeEditor and the read-only CodeViewerPanel.
 */

export const BASE_EDITOR_OPTIONS = {
  fontSize: 13,
  fontFamily: '"JetBrains Mono", "Fira Code", "Cascadia Code", Menlo, Monaco, monospace',
  fontLigatures: true,
  minimap: { enabled: false },
  lineNumbers: "on",
  scrollBeyondLastLine: false,
  renderWhitespace: "none",
  padding: { top: 8, bottom: 8 },
  smoothScrolling: true,
  cursorBlinking: "smooth",
  cursorSmoothCaretAnimation: "on",
  bracketPairColorization: { enabled: true },
  autoClosingBrackets: "always",
  autoClosingQuotes: "always",
  formatOnPaste: true,
  tabSize: 4,
  insertSpaces: true,
  wordWrap: "off",
  folding: true,
  lineDecorationsWidth: 8,
  lineNumbersMinChars: 3,
  glyphMargin: true,
  overviewRulerBorder: false,
  scrollbar: {
    verticalScrollbarSize: 6,
    horizontalScrollbarSize: 6,
    useShadows: false,
  },
};

/**
 * Register custom dark and light themes that use the project's CSS variables
 * so they automatically track the app's theme toggle.
 */
export function defineThemes(monaco) {
  monaco.editor.defineTheme("dsa-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "comment", foreground: "6A9955", fontStyle: "italic" },
      { token: "keyword", foreground: "569CD6" },
      { token: "string", foreground: "CE9178" },
      { token: "number", foreground: "B5CEA8" },
      { token: "type", foreground: "4EC9B0" },
      { token: "identifier", foreground: "D4D4D4" },
      { token: "delimiter", foreground: "808080" },
    ],
    colors: {
      "editor.background": "#1E1E1E",
      "editor.foreground": "#D4D4D4",
      "editor.lineHighlightBackground": "#2A2D2E",
      "editor.selectionBackground": "#264F78",
      "editorLineNumber.foreground": "#858585",
      "editorLineNumber.activeForeground": "#D4D4D4",
      "editor.inactiveSelectionBackground": "#3A3D41",
      "editorCursor.foreground": "#AEAFAD",
      "editorIndentGuide.background1": "#404040",
      "editorIndentGuide.activeBackground1": "#707070",
    },
  });

  monaco.editor.defineTheme("dsa-light", {
    base: "vs",
    inherit: true,
    rules: [
      { token: "comment", foreground: "6A737D", fontStyle: "italic" },
      { token: "keyword", foreground: "CF222E" },
      { token: "string", foreground: "0A3069" },
      { token: "number", foreground: "0550AE" },
      { token: "type", foreground: "953800" },
      { token: "identifier", foreground: "#1F2328" },
      { token: "delimiter", foreground: "#6E7781" },
    ],
    colors: {
      "editor.background": "#ffffff",
      "editor.foreground": "#1F2328",
      "editor.lineHighlightBackground": "#f6f8fa",
      "editor.selectionBackground": "#b6e3ff",
      "editorLineNumber.foreground": "#b0b8c1",
      "editorLineNumber.activeForeground": "#1F2328",
      "editor.inactiveSelectionBackground": "#e2ecf5",
      "editorCursor.foreground": "#1F2328",
      "editorIndentGuide.background1": "#e8ecf0",
      "editorIndentGuide.activeBackground1": "#b0b8c1",
    },
  });
}

/**
 * Map the app theme string to a Monaco theme id.
 * @param {'dark'|'light'} theme
 */
export function themeName(theme) {
  return theme === "dark" ? "dsa-dark" : "dsa-light";
}
