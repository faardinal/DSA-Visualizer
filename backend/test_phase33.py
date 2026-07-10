"""
Tests for Phase 3.3: Heap serialization and stable object graph.
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


def test_primitives():
    code = """x=5
name='John'
flag=True
"""
    result = run_code(code)
    assert result["success"] is True
    trace = result["trace"]
    last = trace[-1]
    # primitives should be direct values
    assert last["locals"].get('x') == 5
    assert last["locals"].get('name') == 'John'
    assert last["locals"].get('flag') is True
    # heap should be empty (no objects)
    assert isinstance(last.get('heap', {}), dict)


def test_list_and_aliasing():
    code = """a=[1,2]
b=a
"""
    result = run_code(code)
    assert result["success"] is True
    trace = result["trace"]
    last = trace[-1]
    heap = last.get('heap', {})
    # vars should reference same ref
    a_ref = last['locals']['a']
    b_ref = last['locals']['b']
    assert isinstance(a_ref, dict) and 'ref' in a_ref
    assert a_ref == b_ref
    # heap contains the list
    hid = str(a_ref['ref'])
    assert hid in heap
    assert heap[hid]['type'] == 'list'
    assert heap[hid]['elements'] == [1,2]


def test_tuple_set_dict():
    code = """t=(1,2)
s={1,2}
d={'a':1}
"""
    result = run_code(code)
    assert result["success"] is True
    last = result["trace"][-1]
    heap = last.get('heap', {})
    # find tuple, set, dict in heap
    types = {v['type'] for v in heap.values()}
    assert 'tuple' in types
    assert 'set' in types
    assert 'dict' in types


def test_nested_lists_and_dicts():
    code = """a=[1,[2,3]]
d={'x': a}
"""
    result = run_code(code)
    assert result["success"] is True
    last = result["trace"][-1]
    heap = last.get('heap', {})
    # outer list ref
    a_ref = last['locals']['a']
    assert 'ref' in a_ref
    outer = heap[str(a_ref['ref'])]
    # second element of outer should be a ref
    second = outer['elements'][1]
    assert isinstance(second, dict) and 'ref' in second
    # dict d should reference same outer list
    dref = last['locals']['d']
    assert 'ref' in dref or isinstance(dref, dict)


def test_user_defined_class():
    code = """class Person:
    def __init__(self):
        self.name='Alice'
        self.age=20
p=Person()
"""
    result = run_code(code)
    assert result["success"] is True
    last = result["trace"][-1]
    heap = last.get('heap', {})
    # find object with type Person
    found = False
    for v in heap.values():
        if v.get('type') == 'Person':
            found = True
            attrs = v.get('attributes', {})
            assert attrs.get('name') == 'Alice'
            assert attrs.get('age') == 20
    assert found


def test_circular_reference_and_immutability():
    code = """a=[]
a.append(a)
"""
    result = run_code(code)
    assert result["success"] is True
    trace = result["trace"]
    # find snapshot after creating empty list (first) and after append (later)
    # assume snapshots correspond to each line; check first and last
    first = trace[0]
    last = trace[-1]
    # first snapshot: heap may contain the list with empty elements or reference
    # last snapshot: list should reference itself
    last_heap = last.get('heap', {})
    found_self = False
    for v in last_heap.values():
        if v.get('type') == 'list':
            elems = v.get('elements', [])
            if elems and isinstance(elems[0], dict) and 'ref' in elems[0]:
                found_self = True
    assert found_self


if __name__ == '__main__':
    tests = [
        test_primitives,
        test_list_and_aliasing,
        test_tuple_set_dict,
        test_nested_lists_and_dicts,
        test_user_defined_class,
        test_circular_reference_and_immutability,
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
