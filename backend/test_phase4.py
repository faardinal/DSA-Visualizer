"""
Phase 4 tests: reliability/validation additions (error_type field, config
clamping, malformed-request handling) and a correctness check that removing
the snapshot heap deepcopy didn't reintroduce cross-snapshot aliasing.

Runs against the live dev server the same way test_phase32.py/test_phase33.py
do (through the Vite proxy on :5000), so both the `Backend` and
`Start application` workflows must be running.
"""
import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://127.0.0.1:5000"


def run_code(code, inputs="", config=None):
    """Helper to POST to /api/run and return (status_code, parsed_json)."""
    body = {"code": code, "inputs": inputs}
    if config is not None:
        body["config"] = config
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        r = urllib.request.urlopen(req)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def test_syntax_error_type():
    """A syntax error should report error_type == 'syntax_error'."""
    status, data = run_code("def f(:\n    pass")
    assert data["success"] is False, data
    assert data.get("error_type") == "syntax_error", data
    return True


def test_runtime_error_type():
    """An uncaught runtime exception should report error_type == 'runtime_error'."""
    status, data = run_code("x = 1 / 0")
    assert data["success"] is False, data
    assert data.get("error_type") == "runtime_error", data
    return True


def test_step_limit_error_type():
    """Exceeding a tiny max_steps should report error_type == 'step_limit'."""
    status, data = run_code(
        "i = 0\nwhile True:\n    i += 1",
        config={"max_steps": 5},
    )
    assert data["success"] is False, data
    assert data.get("error_type") == "step_limit", data
    return True


def test_recursion_limit_error_type():
    """Exceeding a tiny max_recursion_depth should report 'recursion_limit'."""
    code = "def f(n):\n    return f(n + 1)\nf(0)"
    status, data = run_code(code, config={"max_recursion_depth": 3})
    assert data["success"] is False, data
    assert data.get("error_type") == "recursion_limit", data
    return True


def test_config_is_clamped_not_rejected():
    """An absurd config value is clamped server-side rather than erroring out."""
    status, data = run_code("print('hi')", config={"max_steps": 10_000_000_000})
    assert status == 200, (status, data)
    assert data["success"] is True, data
    return True


def test_invalid_request_missing_code():
    """Missing 'code' field returns 400 with error_type 'invalid_request'."""
    payload = json.dumps({}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req)
        assert False, "expected HTTPError"
    except urllib.error.HTTPError as e:
        assert e.code == 400, e.code
        data = json.loads(e.read().decode())
        assert data["success"] is False, data
        assert data.get("error_type") == "invalid_request", data
    return True


def test_invalid_request_wrong_types():
    """Non-string 'code'/'inputs' are rejected as invalid_request, not a 500."""
    for body in ({"code": 123}, {"code": "print(1)", "inputs": 5}):
        payload = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            f"{BASE_URL}/api/run",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req)
            assert False, f"expected HTTPError for {body}"
        except urllib.error.HTTPError as e:
            assert e.code == 400, (body, e.code)
            data = json.loads(e.read().decode())
            assert data.get("error_type") == "invalid_request", data
    return True


def test_heap_snapshots_do_not_alias_after_mutation():
    """
    Regression guard for removing `copy.deepcopy` from snapshot heap
    construction: mutating a list across steps must not retroactively change
    the heap contents already recorded in earlier snapshots.
    """
    code = (
        "nums = [1, 2, 3]\n"
        "a = nums\n"
        "nums.append(4)\n"
        "nums.append(5)\n"
    )
    status, data = run_code(code)
    assert data["success"] is True, data
    trace = data["trace"]

    def heap_list_values(snapshot):
        for entry in snapshot.get("heap", {}).values():
            if entry.get("type") == "list":
                return entry.get("elements")
        return None

    # Find the earliest snapshot where the list has exactly 3 elements
    # and confirm a later snapshot's mutation didn't rewrite it in place.
    early = next((s for s in trace if heap_list_values(s) == [1, 2, 3]), None)
    late = next((s for s in trace if heap_list_values(s) == [1, 2, 3, 4, 5]), None)
    assert early is not None, "expected an early snapshot with [1, 2, 3]"
    assert late is not None, "expected a later snapshot with [1, 2, 3, 4, 5]"
    # Re-check the early snapshot's value is still [1, 2, 3] after computing
    # `late` (i.e. it wasn't a shared/aliased list mutated out from under us).
    assert heap_list_values(early) == [1, 2, 3], heap_list_values(early)
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Phase 4 Reliability Tests")
    print("=" * 50)

    tests = [
        test_syntax_error_type,
        test_runtime_error_type,
        test_step_limit_error_type,
        test_recursion_limit_error_type,
        test_config_is_clamped_not_rejected,
        test_invalid_request_missing_code,
        test_invalid_request_wrong_types,
        test_heap_snapshots_do_not_alias_after_mutation,
    ]

    all_passed = True
    for test in tests:
        try:
            test()
            print(f"  PASSED: {test.__name__}")
        except Exception as e:
            print(f"  FAILED: {test.__name__}: {e}")
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)
