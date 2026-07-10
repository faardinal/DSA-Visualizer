"""
Test for Phase 3.4.1: Recursion depth limit enforcement.
"""
import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:5000"


def run_code(code, inputs="", config=None):
    payload = {"code": code}
    if inputs:
        payload["inputs"] = inputs
    if config:
        payload["config"] = config
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/run", data=data, headers={"Content-Type": "application/json"}, method="POST")
    r = urllib.request.urlopen(req)
    return json.loads(r.read().decode())


def test_recursion_limit_exceeded():
    """Infinite recursion should stop immediately with a clean error, not hang or crash."""
    code = """def recurse(n):
    return recurse(n + 1)

recurse(0)
"""
    result = run_code(code, config={"max_recursion_depth": 50})
    assert result["success"] is False
    error = result["error"]
    assert "Recursion depth limit exceeded" in error
    assert "50" in error
    # Execution must have actually stopped: trace should not be unbounded.
    assert len(result["trace"]) > 0


def test_recursion_within_limit_succeeds():
    """Recursion that stays under the limit should execute normally."""
    code = """def countdown(n):
    if n <= 0:
        return 0
    return countdown(n - 1)

result = countdown(10)
"""
    result = run_code(code, config={"max_recursion_depth": 100})
    assert result["success"] is True


def test_normal_execution_unaffected():
    """Non-recursive code must be unaffected by the recursion limit change."""
    code = """x = 1
y = 2
z = x + y
"""
    result = run_code(code)
    assert result["success"] is True


if __name__ == '__main__':
    tests = [
        test_recursion_limit_exceeded,
        test_recursion_within_limit_succeeds,
        test_normal_execution_unaffected,
    ]
    all_passed = True
    for t in tests:
        try:
            t()
            print(t.__name__, 'PASSED')
        except Exception as e:
            print(t.__name__, 'FAILED:', e)
            import traceback; traceback.print_exc()
            all_passed = False
    if all_passed:
        print('ALL TESTS PASSED')
        sys.exit(0)
    else:
        print('SOME TESTS FAILED')
        sys.exit(1)
