"""Dedicated process entry point for a single untrusted submission."""

from dataclasses import asdict
import json
import os
import sys

from backend.models import ExecutionConfig
from backend.tracer import _apply_worker_resource_limits, execute_python


def _snapshot_payload(snapshot):
    return {
        "step": snapshot.step,
        "event": snapshot.event,
        "line": snapshot.line,
        "function": snapshot.function,
        "filename": snapshot.filename,
        "code": snapshot.code,
        "locals": snapshot.locals,
        "globals": snapshot.globals,
        "stdout": snapshot.stdout,
        "exception": snapshot.exception,
        "heap": snapshot.heap,
        "frame_id": snapshot.frame_id,
        "call_stack": snapshot.call_stack,
        "return_value": snapshot.return_value,
        "has_return_value": snapshot.has_return_value,
    }


def main():
    try:
        payload = json.load(sys.stdin)
        config = ExecutionConfig(**payload.get("config", {}))
        os.environ.clear()
        _apply_worker_resource_limits(config)
        snapshots, error, execution_time, error_type = execute_python(
            payload["code"], payload.get("inputs", ""), config
        )
        print(json.dumps({
            "snapshots": [_snapshot_payload(snapshot) for snapshot in snapshots],
            "error": error,
            "execution_time": execution_time,
            "error_type": error_type,
        }))
    except MemoryError:
        print(json.dumps({"snapshots": [], "error": "Memory limit exceeded", "execution_time": 0.0, "error_type": "memory_limit"}))
    except BaseException as exc:
        print(json.dumps({"snapshots": [], "error": f"Sandbox worker failed: {type(exc).__name__}: {exc}", "execution_time": 0.0, "error_type": "runtime_error"}))


if __name__ == "__main__":
    main()
