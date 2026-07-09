import { adaptBackendTrace } from "./adaptBackendTrace";
import { toast } from "@/components/ui/use-toast";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "/api";

/**
 * Toast copy per backend `error_type`. Falls back to a generic "Run failed"
 * for unknown/missing types so older backend responses (or ones we haven't
 * special-cased) still show something reasonable.
 */
const ERROR_TITLES = {
  syntax_error: "Syntax error",
  runtime_error: "Runtime error",
  step_limit: "Step limit reached",
  time_limit: "Timed out",
  recursion_limit: "Recursion limit reached",
  invalid_request: "Invalid request",
  server_error: "Server error",
};

/**
 * Runs code against the real backend and adapts the response into the
 * frontend's internal trace format. No more silent fallback to a canned
 * mock trace on failure — if the backend is unreachable or errors, the
 * caller is told via the returned `error` and a toast, and the caller
 * should keep whatever trace it already had rather than pretending a
 * demo trace is a real result.
 */
export async function runCode(code, inputs = "", { signal } = {}) {
  try {
    const res = await fetch(`${BACKEND_URL}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, inputs }),
      signal,
    });

    if (!res.ok && res.status >= 500) {
      // A non-2xx status with no parseable error body (proxy/server crash)
      // is a backend-unavailable situation, distinct from an execution
      // error the backend deliberately reported with a 200/400.
      throw new Error(`Backend responded with ${res.status}`);
    }

    const data = await res.json();

    if (!data.success) {
      toast({
        title: ERROR_TITLES[data.error_type] || "Run failed",
        description: data.error || "The backend could not execute this code.",
        variant: "destructive",
      });
      // The backend still returns whatever partial trace it captured before
      // failing (e.g. steps up to and including an exception) — keep it
      // inspectable instead of throwing it away.
      return {
        trace: Array.isArray(data.trace) ? adaptBackendTrace(data.trace) : null,
        error: data.error,
        errorType: data.error_type,
        demoMode: false,
      };
    }

    return {
      trace: adaptBackendTrace(data.trace),
      demoMode: false,
      executionTime: data.execution_time,
    };
  } catch (err) {
    if (err.name === "AbortError") {
      // User-initiated Stop — not a failure, so no error toast. The backend
      // keeps executing to completion server-side (there is no mid-run
      // cancellation API), but the frontend simply stops waiting for it.
      return { trace: null, error: null, errorType: "aborted", demoMode: false, aborted: true };
    }
    toast({
      title: "Couldn't reach the backend",
      description: err.message || "The request failed.",
      variant: "destructive",
    });
    return { trace: null, error: err.message, errorType: "backend_unreachable", demoMode: false };
  }
}
