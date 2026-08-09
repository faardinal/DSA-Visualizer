"""
STEP 3 verification: all 7 problems through the ISOLATED execution path.

For each registered problem we confirm all four LeetCode verdicts map correctly:
  * ACCEPTED          — a correct solution
  * WRONG_ANSWER      — an incorrect solution
  * RUNTIME_ERROR     — a crashing solution
  * TIME_LIMIT_EXCEEDED — an infinite / too-slow solution

Also confirms the visualizer/tracing path still produces a trace.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.execution_engine import get_registry, run_solution
from backend.models import ExecutionConfig

# Server-side submission-style config, with a tight timeout for the TLE cases.
SUBMIT = ExecutionConfig(max_time_seconds=1.0, max_steps=50_000,
                         max_recursion_depth=800, max_output_chars=10_000)


def _run(source, problem_id, config=SUBMIT):
    return run_solution(source, problem_id=problem_id, config=config).to_dict()


# Correct solutions for each problem.
CORRECT = {
    "two-sum": '''class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, v in enumerate(nums):
            if target - v in seen:
                return [seen[target - v], i]
            seen[v] = i
        return []
''',
    "binary-search": '''class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
''',
    "valid-parentheses": '''class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for c in s:
            if c in pairs:
                if not stack or stack.pop() != pairs[c]:
                    return False
            else:
                stack.append(c)
        return not stack
''',
    "merge-sorted-array": '''class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, k = m - 1, n - 1, m + n - 1
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]; i -= 1
            else:
                nums1[k] = nums2[j]; j -= 1
            k -= 1
        while j >= 0:
            nums1[k] = nums2[j]; j -= 1; k -= 1
''',
    "reverse-linked-list": '''class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        while head:
            nxt = head.next
            head.next = prev
            prev = head
            head = nxt
        return prev
''',
    "max-depth-binary-tree": '''class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
''',
    "number-of-islands": '''class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0
        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
                return
            grid[r][c] = "0"
            dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    dfs(r, c)
        return count
''',
}

# Wrong solutions (deterministically wrong for at least the visible examples).
WRONG = {
    "two-sum": "class Solution:\n    def twoSum(self, nums, target):\n        return [0, 0]\n",
    "binary-search": "class Solution:\n    def search(self, nums, target):\n        return -1\n",
    "valid-parentheses": "class Solution:\n    def isValid(self, s):\n        return False\n",
    "merge-sorted-array": "class Solution:\n    def merge(self, nums1, m, nums2, n):\n        return None\n",
    "reverse-linked-list": "class Solution:\n    def reverseList(self, head):\n        return head\n",
    "max-depth-binary-tree": "class Solution:\n    def maxDepth(self, root):\n        return 0\n",
    "number-of-islands": "class Solution:\n    def numIslands(self, grid):\n        return 0\n",
}

# Crashing solutions: divide by zero inside the method.
CRASH = {
    pid: "class Solution:\n    def %s(self, *a):\n        return 1 // 0\n" %
         get_registry().get(pid).method_name
    for pid in CORRECT
}

# Infinite-loop solution per problem method.
LOOP = {
    pid: "class Solution:\n    def %s(self, *a):\n        while True:\n            pass\n" %
         get_registry().get(pid).method_name
    for pid in CORRECT
}


RESULTS = []


def check(name, condition, detail=""):
    RESULTS.append((name, condition, detail))
    tag = "PASS" if condition else "FAIL"
    print(f"  {tag}  {name}" + (f"  ({detail})" if detail else ""))


problem_ids = get_registry().get_all_problem_ids()
print(f"Registered problems ({len(problem_ids)}): {problem_ids}\n")

assert set(CORRECT) == set(problem_ids), "Correct-solution set must match registry"

for pid in problem_ids:
    print(f"=== {pid} ===")

    # ACCEPTED
    r = _run(CORRECT[pid], pid)
    check(f"{pid}: correct -> ACCEPTED", r["status"] == "ACCEPTED", r["status"])

    # WRONG_ANSWER
    r = _run(WRONG[pid], pid)
    check(f"{pid}: wrong -> WRONG_ANSWER", r["status"] == "WRONG_ANSWER", r["status"])

    # RUNTIME_ERROR
    r = _run(CRASH[pid], pid)
    check(f"{pid}: crash -> RUNTIME_ERROR", r["status"] == "RUNTIME_ERROR", r["status"])

    # TIME_LIMIT_EXCEEDED
    r = _run(LOOP[pid], pid)
    check(f"{pid}: infinite loop -> TIME_LIMIT_EXCEEDED", r["status"] == "TIME_LIMIT_EXCEEDED", r["status"])

    # Visualizer path: a correct solution must still produce a non-empty trace.
    r = _run(CORRECT[pid], pid, config=ExecutionConfig(max_time_seconds=2.0, max_steps=200_000))
    check(f"{pid}: trace generated", isinstance(r.get("trace"), list) and len(r["trace"]) > 0,
          f"trace len={len(r.get('trace') or [])}")


print("\n=== SUMMARY ===")
passed = sum(1 for _, ok, _ in RESULTS if ok)
failed = sum(1 for _, ok, _ in RESULTS if not ok)
for name, ok, detail in RESULTS:
    if not ok:
        print(f"  FAILED: {name}  ({detail})")
print(f"\n{passed} passed, {failed} failed out of {len(RESULTS)} checks")
if failed:
    raise SystemExit(1)
