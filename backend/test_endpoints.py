"""Test script for backend endpoints."""
import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test GET /api/health"""
    print("Testing GET /api/health...")
    r = urllib.request.urlopen(f"{BASE_URL}/api/health")
    data = json.loads(r.read().decode())
    print(f"  Response: {data}")
    assert data == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {data}"
    print("  PASSED!")
    return True

def test_run_valid():
    """Test POST /api/run with valid code"""
    print("Testing POST /api/run (valid code)...")
    payload = json.dumps({"code": "print('hello')"}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    r = urllib.request.urlopen(req)
    data = json.loads(r.read().decode())
    print(f"  Response: {data}")
    assert data["success"] == True, f"Expected success=True, got {data}"
    assert data["message"] == "Backend ready", f"Expected 'Backend ready', got {data['message']}"
    assert data["trace"] == [], f"Expected empty trace, got {data['trace']}"
    print("  PASSED!")
    return True

def test_run_no_code():
    """Test POST /api/run with no code (error case)"""
    print("Testing POST /api/run (no code - error case)...")
    payload = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        r = urllib.request.urlopen(req)
        data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        data = json.loads(e.read().decode())
        print(f"  Response (HTTP {e.code}): {data}")
        assert data["success"] == False, f"Expected success=False, got {data}"
        assert "error" in data, f"Expected error field, got {data}"
        print("  PASSED!")
        return True

def test_run_invalid_json():
    """Test POST /api/run with invalid JSON (error case)"""
    print("Testing POST /api/run (invalid JSON - error case)...")
    req = urllib.request.Request(
        f"{BASE_URL}/api/run",
        data=b"not json",
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        r = urllib.request.urlopen(req)
        data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        data = json.loads(e.read().decode())
        print(f"  Response (HTTP {e.code}): {data}")
        assert data["success"] == False, f"Expected success=False, got {data}"
        assert "error" in data, f"Expected error field, got {data}"
        print("  PASSED!")
        return True

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Endpoint Tests")
    print("=" * 50)
    
    all_passed = True
    tests = [
        test_health,
        test_run_valid,
        test_run_no_code,
        test_run_invalid_json,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"  FAILED: {e}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)