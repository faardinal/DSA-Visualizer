"""
Comprehensive test script for Phase 3.2: Execution Tracing.
Tests the backend's ability to execute Python code and capture execution traces.
"""
import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:5000"


def run_code(code, inputs=""):
    """Helper to run code and return the response."""
    payload = json.dumps({"code": code, "inputs": inputs}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    r = urllib.request.urlopen(req)
    return json.loads(r.read().decode())


def test_example1_simple_variables():
    """Example 1: Simple variable assignment and arithmetic"""
    print("Test 1: Simple variables and arithmetic")
    print("-" * 40)
    code = """x=5
y=8
z=x+y
print(z)"""
    
    result = run_code(code)
    print(f"  Success: {result.get('success')}")
    print(f"  Trace steps: {len(result.get('trace', []))}")
    
    assert result["success"] == True, f"Expected success=True, got {result}"
    trace = result["trace"]
    assert len(trace) > 0, "Expected non-empty trace"
    
    # Check that we have line events
    line_events = [s for s in trace if s["event"] == "line"]
    assert len(line_events) > 0, "Expected at least one line event"
    
    # Check that print output is captured
    last_snapshot = trace[-1]
    assert "13" in last_snapshot["stdout"], f"Expected '13' in stdout, got: {last_snapshot['stdout']}"
    
    # Check that z is in globals (module level)
    module_snapshots = [s for s in trace if s["function"] == "<module>"]
    assert len(module_snapshots) > 0, "Expected module-level snapshots"
    
    print("  PASSED!")
    return True


def test_example2_loop():
    """Example 2: For loop with print"""
    print("\nTest 2: For loop with print")
    print("-" * 40)
    code = """for i in range(3):
    print(i)"""
    
    result = run_code(code)
    print(f"  Success: {result.get('success')}")
    print(f"  Trace steps: {len(result.get('trace', []))}")
    
    assert result["success"] == True, f"Expected success=True, got {result}"
    trace = result["trace"]
    assert len(trace) > 0, "Expected non-empty trace"
    
    # Check that all numbers are printed
    last_snapshot = trace[-1]
    stdout = last_snapshot["stdout"]
    assert "0" in stdout, "Expected '0' in stdout"
    assert "1" in stdout, "Expected '1' in stdout"
    assert "2" in stdout, "Expected '2' in stdout"
    
    print("  PASSED!")
    return True


def test_example3_function():
    """Example 3: Function definition and call"""
    print("\nTest 3: Function definition and call")
    print("-" * 40)
    code = """def add(a,b):
    return a+b

print(add(3,4))"""
    
    result = run_code(code)
    print(f"  Success: {result.get('success')}")
    print(f"  Trace steps: {len(result.get('trace', []))}")
    
    assert result["success"] == True, f"Expected success=True, got {result}"
    trace = result["trace"]
    assert len(trace) > 0, "Expected non-empty trace"
    
    # Check that we have snapshots from both module and add function
    functions = set(s["function"] for s in trace)
    assert "add" in functions, f"Expected 'add' function in trace, got: {functions}"
    assert "<module>" in functions, f"Expected '<module>' in trace, got: {functions}"
    
    # Check that print output contains 7
    last_snapshot = trace[-1]
    assert "7" in last_snapshot["stdout"], f"Expected '7' in stdout, got: {last_snapshot['stdout']}"
    
    # Check return event
    return_events = [s for s in trace if s["event"] == "return"]
    assert len(return_events) > 0, "Expected at least one return event"
    
    print("  PASSED!")
    return True


def test_example4_exception():
    """Example 4: Division by zero exception"""
    print("\nTest 4: Division by zero exception")
    print("-" * 40)
    code = """1/0"""
    
    result = run_code(code)
    print(f"  Success: {result.get('success')}")
    print(f"  Error: {result.get('error')}")
    
    # Should have success=false due to exception
    assert result["success"] == False, f"Expected success=False, got {result}"
    
    # Should have error information
    assert "error" in result, "Expected error field in response"
    assert "ZeroDivisionError" in result["error"], f"Expected ZeroDivisionError in error, got: {result['error']}"
    
    # Should have exception event in trace
    trace = result["trace"]
    exception_events = [s for s in trace if s["event"] == "exception"]
    assert len(exception_events) > 0, "Expected at least one exception event"
    
    print("  PASSED!")
    return True


def test_primitive_serialization():
    """Test that only primitive values are serialized correctly"""
    print("\nTest 5: Primitive serialization")
    print("-" * 40)
    code = """a = 42
b = 3.14
c = "hello"
d = True
e = None
f = [1, 2, 3]
g = {"key": "value"}"""
    
    result = run_code(code)
    print(f"  Success: {result.get('success')}")
    
    assert result["success"] == True, f"Expected success=True, got {result}"
    trace = result["trace"]
    
    # Find a snapshot with all variables
    last_snapshot = trace[-1]
    globals_dict = last_snapshot.get("globals", {})
    
    # Check primitives are serialized correctly
    assert globals_dict.get("a") == 42, f"Expected a=42, got {globals_dict.get('a')}"
    assert globals_dict.get("b") == 3.14, f"Expected b=3.14, got {globals_dict.get('b')}"
    assert globals_dict.get("c") == "hello", f"Expected c='hello', got {globals_dict.get('c')}"
    assert globals_dict.get("d") == True, f"Expected d=True, got {globals_dict.get('d')}"
    assert globals_dict.get("e") is None, f"Expected e=None, got {globals_dict.get('e')}"
    
    # Phase 3.3: non-primitives are serialized as heap references, not "unsupported"
    heap = last_snapshot.get("heap", {})
    f_ref = globals_dict.get("f")
    g_ref = globals_dict.get("g")
    assert isinstance(f_ref, dict) and "ref" in f_ref, f"Expected f as heap ref, got {f_ref}"
    assert isinstance(g_ref, dict) and "ref" in g_ref, f"Expected g as heap ref, got {g_ref}"
    assert heap[str(f_ref["ref"])] == {"type": "list", "elements": [1, 2, 3]}, f"Unexpected heap entry for f: {heap.get(str(f_ref['ref']))}"
    assert heap[str(g_ref["ref"])] == {"type": "dict", "entries": [["key", "value"]]}, f"Unexpected heap entry for g: {heap.get(str(g_ref['ref']))}"
    
    print("  PASSED!")
    return True


def test_stdin_input():
    """Test that stdin input works"""
    print("\nTest 6: Stdin input")
    print("-" * 40)
    code = """name = input()
print("Hello, " + name)"""
    
    result = run_code(code, inputs="World")
    print(f"  Success: {result.get('success')}")
    
    assert result["success"] == True, f"Expected success=True, got {result}"
    trace = result["trace"]
    
    # Check that output contains the greeting
    last_snapshot = trace[-1]
    assert "Hello, World" in last_snapshot["stdout"], f"Expected 'Hello, World' in stdout, got: {last_snapshot['stdout']}"
    
    print("  PASSED!")
    return True


def test_execution_limits():
    """Test that execution limits are enforced"""
    print("\nTest 7: Execution limits (step limit)")
    print("-" * 40)
    # Infinite loop that should be stopped by step limit
    code = """while True:
    pass"""
    
    # Use a small step limit to make the test fast
    payload = json.dumps({
        "code": code,
        "config": {"max_steps": 100}
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    r = urllib.request.urlopen(req)
    result = json.loads(r.read().decode())
    
    print(f"  Success: {result.get('success')}")
    print(f"  Error: {result.get('error')}")
    
    # Should have stopped due to step limit
    assert result["success"] == False, "Expected success=False due to step limit"
    assert "Step limit exceeded" in result.get("error", ""), f"Expected step limit error, got: {result.get('error')}"
    
    print("  PASSED!")
    return True


def test_snapshot_format():
    """Test that snapshot format matches the specification"""
    print("\nTest 8: Snapshot format validation")
    print("-" * 40)
    code = """x = 5"""
    
    result = run_code(code)
    assert result["success"] == True
    
    trace = result["trace"]
    assert len(trace) > 0
    
    snapshot = trace[0]
    
    # Check required fields
    required_fields = ["step", "event", "line", "function", "code", "locals", "globals", "stdout"]
    for field in required_fields:
        assert field in snapshot, f"Missing required field: {field}"
    
    # Check field types
    assert isinstance(snapshot["step"], int), "step should be int"
    assert isinstance(snapshot["event"], str), "event should be str"
    assert isinstance(snapshot["line"], int), "line should be int"
    assert isinstance(snapshot["function"], str), "function should be str"
    assert isinstance(snapshot["code"], str), "code should be str"
    assert isinstance(snapshot["locals"], dict), "locals should be dict"
    assert isinstance(snapshot["globals"], dict), "globals should be dict"
    assert isinstance(snapshot["stdout"], str), "stdout should be str"
    
    print("  PASSED!")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3.2: Execution Tracing Tests")
    print("=" * 60)
    
    all_passed = True
    tests = [
        test_example1_simple_variables,
        test_example2_loop,
        test_example3_function,
        test_example4_exception,
        test_primitive_serialization,
        test_stdin_input,
        test_execution_limits,
        test_snapshot_format,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"  FAILED: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)