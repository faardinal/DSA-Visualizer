import React from "react";
import { AlertTriangle, RotateCcw } from "lucide-react";

export default class AppErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error("Visualizer render failed", error, info);
  }

  render() {
    if (!this.state.error) return this.props.children;

    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-6">
        <div className="w-full max-w-xl rounded-md border border-destructive/30 bg-card p-5 shadow-sm">
          <div className="flex items-center gap-2 text-destructive mb-3">
            <AlertTriangle className="w-5 h-5" />
            <h1 className="text-sm font-semibold">Visualizer error</h1>
          </div>
          <p className="text-sm text-muted-foreground mb-3">
            Something failed while rendering the visualization. Your app is still running.
          </p>
          <pre className="max-h-40 overflow-auto rounded bg-muted p-3 text-xs text-muted-foreground whitespace-pre-wrap mb-4">
            {this.state.error.message}
          </pre>
          <button
            type="button"
            onClick={() => this.setState({ error: null })}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-3 py-2 text-xs font-medium text-primary-foreground hover:opacity-90"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset view
          </button>
        </div>
      </div>
    );
  }
}
