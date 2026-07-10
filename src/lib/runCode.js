/**
 * runCode.js
 * Sends code to the backend execution engine and returns the trace.
 *
 * In development the Vite proxy forwards /api/* to localhost:8000.
 * In production (Vercel) VITE_API_BASE_URL must be set to the Render URL.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

/**
 * @param {string} code       - Python source code
 * @param {string} [inputs]   - Optional stdin input string
 * @param {object} [config]   - Optional { max_steps, max_time_seconds, max_recursion_depth }
 * @param {object} [options]  - Optional fetch options, currently { signal }
 * @returns {Promise<object>} - { success, trace, error?, execution_time }
 */
export async function runCode(code, inputs = '', config = {}, options = {}) {
  const { signal: legacySignal, ...executionConfig } = config || {};
  const signal = options.signal || legacySignal;

  const response = await fetch(`${API_BASE}/api/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, inputs, config: executionConfig }),
    signal,
  });

  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    throw new Error(`Backend returned invalid JSON (${response.status})`);
  }

  if (!response.ok) {
    const message = data?.error || data?.message || text || response.statusText;
    throw new Error(`Backend error ${response.status}: ${message}`);
  }

  return data;
}

/**
 * Check backend health.
 * @returns {Promise<boolean>}
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    const data = await response.json();
    return data.status === 'ok';
  } catch {
    return false;
  }
}
