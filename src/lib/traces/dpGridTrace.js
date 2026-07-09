// DP Grid trace — demonstrates cell fill with dependency highlighting.
// Unique Paths problem: dp[i][j] = dp[i-1][j] + dp[i][j-1]
// Current cell highlighted strongly, dependency cells highlighted softly.

export const DP_GRID_CODE = `# Unique Paths in a Grid
m, n = 3, 3
dp = [[1] * n for _ in range(m)]
for i in range(1, m):
    for j in range(1, n):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
print(dp[m-1][n-1])`;

const r = (id) => ({ ref: id });
const v = (val) => ({ value: val });
const h = (id, type, value) => ({ id, type, value });
const f = (frame_id, func, vars) => ({ frame_id, func, vars });

const mod = (extra = {}) => f("frame_mod", "<module>", extra);

const grid = (vals) => h("grid_dp", "grid", vals);

const hl = (row, col, reason) => ({ objectId: "grid_dp", path: [row, col], metadata: { reason } });

export const dpGridTrace = [
  // 0: Initialize grid — first row and col are all 1s
  { step: 0, line: 3, code: "dp = [[1] * n for _ in range(m)]", locals: [mod({ dp: r("grid_dp"), m: v(3), n: v(3) })], globals: { dp: r("grid_dp"), m: v(3), n: v(3) }, heap: [grid([[1, 1, 1], [1, 0, 0], [1, 0, 0]])], stdout: "" },

  // 1: i=1, j=1 → dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
  { step: 1, line: 6, code: "dp[i][j] = dp[i-1][j] + dp[i][j-1]", locals: [mod({ dp: r("grid_dp"), m: v(3), n: v(3), i: v(1), j: v(1) })], globals: { dp: r("grid_dp"), m: v(3), n: v(3) }, heap: [grid([[1, 1, 1], [1, 2, 0], [1, 0, 0]])], highlights: [hl(1, 1, "current"), hl(0, 1, "dependency"), hl(1, 0, "dependency")], stdout: "" },

  // 2: i=1, j=2 → dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3
  { step: 2, line: 6, code: "dp[i][j] = dp[i-1][j] + dp[i][j-1]", locals: [mod({ dp: r("grid_dp"), m: v(3), n: v(3), i: v(1), j: v(2) })], globals: { dp: r("grid_dp"), m: v(3), n: v(3) }, heap: [grid([[1, 1, 1], [1, 2, 3], [1, 0, 0]])], highlights: [hl(1, 2, "current"), hl(0, 2, "dependency"), hl(1, 1, "dependency")], stdout: "" },

  // 3: i=2, j=1 → dp[2][1] = dp[1][1] + dp[2][0] = 2 + 1 = 3
  { step: 3, line: 6, code: "dp[i][j] = dp[i-1][j] + dp[i][j-1]", locals: [mod({ dp: r("grid_dp"), m: v(3), n: v(3), i: v(2), j: v(1) })], globals: { dp: r("grid_dp"), m: v(3), n: v(3) }, heap: [grid([[1, 1, 1], [1, 2, 3], [1, 3, 0]])], highlights: [hl(2, 1, "current"), hl(1, 1, "dependency"), hl(2, 0, "dependency")], stdout: "" },

  // 4: i=2, j=2 → dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6
  { step: 4, line: 6, code: "dp[i][j] = dp[i-1][j] + dp[i][j-1]", locals: [mod({ dp: r("grid_dp"), m: v(3), n: v(3), i: v(2), j: v(2) })], globals: { dp: r("grid_dp"), m: v(3), n: v(3) }, heap: [grid([[1, 1, 1], [1, 2, 3], [1, 3, 6]])], highlights: [hl(2, 2, "current"), hl(1, 2, "dependency"), hl(2, 1, "dependency")], stdout: "" },

  // 5: print(dp[m-1][n-1]) → 6
  { step: 5, line: 7, code: "print(dp[m-1][n-1])", locals: [mod({ dp: r("grid_dp"), m: v(3), n: v(3) })], globals: { dp: r("grid_dp"), m: v(3), n: v(3) }, heap: [grid([[1, 1, 1], [1, 2, 3], [1, 3, 6]])], stdout: "6" },
];