/**
 * runSolution.js
 * API client for the LeetCode-style execution engine.
 */
const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

/**
 * Run a LeetCode-style solution against hidden tests.
 * @param {string} code - Python source containing class Solution
 * @param {object} [opts] - { problemId?, method?, replayTestIdx?, config? }
 * @param {object} [options] - { signal }
 * @returns {Promise<object>} - { success, passed, test_results, statistics, trace, ... }
 */
export async function runSolution(code, opts = {}, options = {}) {
  const { problemId, method, replayTestIdx, config } = opts;
  const body = { code };
  if (problemId) body.problem_id = problemId;
  if (method) body.method = method;
  if (replayTestIdx != null) body.replay_test_idx = replayTestIdx;
  if (config) body.config = config;

  const response = await fetch(`${API_BASE}/api/run-solution`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal: options.signal,
  });

  const text = await response.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch {
    throw new Error(`Backend returned invalid JSON (${response.status})`);
  }
  if (!response.ok) {
    throw new Error(data?.error || `Backend error ${response.status}`);
  }
  return data;
}

/**
 * Fetch the list of registered problems.
 * @returns {Promise<Array>} - [{ problem_id, title, method_name, difficulty, pattern }]
 */
export async function fetchProblems() {
  try {
    const response = await fetch(`${API_BASE}/api/problems`);
    const data = await response.json();
    return data.problems || [];
  } catch {
    return [];
  }
}
