/**
 * adaptSolutionTrace.js
 * Adapts the LeetCode execution result into the frontend's internal schema.
 * Reuses adaptBackendTrace for the trace portion (same snapshot format).
 */
import { adaptBackendTrace } from './adaptBackendTrace';

/**
 * @param {object} raw - Raw response from POST /api/run-solution
 * @returns {object} - { trace, testResults, statistics, passed, ... }
 */
export function adaptSolutionResult(raw) {
  if (!raw) return emptyResult();

  const trace = adaptBackendTrace(raw.trace || []);
  const testResults = (raw.test_results || []).map(normalizeTestResult);
  const statistics = raw.statistics || null;

  return {
    trace,
    testResults,
    statistics,
    passed: Boolean(raw.passed),
    methodDetected: raw.method_detected || '',
    problemId: raw.problem_id || null,
    problemTitle: raw.problem_title || null,
    ambiguousProblems: raw.ambiguous_problems || null,
    traceTestIdx: raw.trace_test_idx ?? 0,
    error: raw.error || null,
    errorType: raw.error_type || null,
    executionTime: raw.execution_time ?? raw.total_time ?? null,
    status: raw.status || null,
    seed: raw.seed ?? null,
    sessionId: raw.session_id || raw.trace_id || null,
  };
}

function normalizeTestResult(r) {
  return {
    testIdx: r.test_idx,
    description: r.description,
    passed: Boolean(r.passed),
    expected: r.expected,
    actual: r.actual,
    inputRepr: r.input_repr || '',
    consoleOutput: r.console_output || '',
    exception: r.exception || null,
    traceback: r.traceback || null,
    executionTime: r.execution_time ?? null,
    memoryBytes: r.memory_bytes ?? null,
  };
}

function emptyResult() {
  return {
    trace: [], testResults: [], statistics: null, passed: false,
    methodDetected: '', problemId: null, problemTitle: null,
    ambiguousProblems: null, traceTestIdx: 0,
    error: null, errorType: null, executionTime: null,
  };
}
