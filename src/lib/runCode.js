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
 * @returns {Promise<object>} - { success, trace, error?, execution_time }
 */
export async function runCode(code, inputs = '', config = {}) {
  const response = await fetch(`${API_BASE}/api/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, inputs, config }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Backend error ${response.status}: ${text}`);
  }

  return response.json();
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
