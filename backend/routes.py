"""
Flask routes for the execution API.
Phase 3.2: Execution tracing with primitive-only serialization.
"""
from flask import Blueprint, request, jsonify
import time

from .tracer import execute_python
from .models import ExecutionConfig

# Create blueprint
execution_bp = Blueprint('execution', __name__, url_prefix='/api')


def snapshot_to_dict(snapshot) -> dict:
    """Convert Snapshot dataclass to dictionary for JSON response."""
    result = {
        "step": snapshot.step,
        "event": snapshot.event,
        "line": snapshot.line,
        "function": snapshot.function,
        "code": snapshot.code,
        "locals": snapshot.locals,
        "globals": snapshot.globals,
        "stdout": snapshot.stdout,
        "heap": snapshot.heap,
        "frame_id": snapshot.frame_id,
        "call_stack": snapshot.call_stack,
    }
    if snapshot.exception:
        result["exception"] = snapshot.exception
    if snapshot.has_return_value:
        result["return_value"] = snapshot.return_value
    return result


@execution_bp.route('/run', methods=['POST'])
def run_code():
    """
    Execute Python code and return execution trace.

    Request:
    {
        "code": "python code string",
        "inputs": "optional stdin input",
        "config": {
            "max_steps": 10000,
            "max_time_seconds": 30,
            "max_recursion_depth": 1000
        }
    }

    Response (success):
    {
        "success": true,
        "trace": [
            {
                "step": 1,
                "event": "line",
                "line": 1,
                "function": "<module>",
                "code": "x = 5",
                "locals": {},
                "globals": {"x": 5},
                "stdout": ""
            },
            ...
        ]
    }

    Response (error):
    {
        "success": false,
        "trace": [...],
        "error": {
            "type": "ZeroDivisionError",
            "message": "division by zero",
            "line": 3
        }
    }
    """
    start_time = time.time()

    try:
        # Validate JSON request
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({
                "success": False,
                "trace": [],
                "error": "Invalid JSON request",
                "error_type": "invalid_request"
            }), 400

        # Get code
        code = data.get('code', '')
        if not code or not isinstance(code, str):
            return jsonify({
                "success": False,
                "trace": [],
                "error": "No code provided",
                "error_type": "invalid_request"
            }), 400

        # Get optional inputs
        inputs = data.get('inputs', '')
        if not isinstance(inputs, str):
            return jsonify({
                "success": False,
                "trace": [],
                "error": "'inputs' must be a string",
                "error_type": "invalid_request"
            }), 400

        # Get optional config. Unrecognized/malformed config fields fall back
        # to defaults instead of raising, out-of-range values are clamped by
        # ExecutionConfig itself.
        config_data = data.get('config') or {}
        if not isinstance(config_data, dict):
            config_data = {}
        config = ExecutionConfig(
            max_steps=config_data.get('max_steps', 10000),
            max_time_seconds=config_data.get('max_time_seconds', 30.0),
            max_recursion_depth=config_data.get('max_recursion_depth', 1000)
        )

        # Execute code
        snapshots, error, exec_time, error_type = execute_python(code, inputs, config)

        # Convert snapshots to dict
        trace = [snapshot_to_dict(s) for s in snapshots]

        # Build response
        if error:
            # Execution had an error. `error_type` is additive metadata for
            # the frontend to branch on; `error` remains the human-readable
            # string for backward compatibility with older clients.
            response = {
                "success": False,
                "trace": trace,
                "error": error,
                "error_type": error_type or "runtime_error",
                "execution_time": exec_time
            }
        else:
            # Successful execution
            response = {
                "success": True,
                "trace": trace,
                "execution_time": exec_time
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "trace": [],
            "error": f"Server error: {str(e)}",
            "error_type": "server_error",
            "execution_time": time.time() - start_time
        }), 500


@execution_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok"
    })


@execution_bp.route('/config', methods=['GET'])
def get_config():
    """Get default execution configuration."""
    config = ExecutionConfig()
    return jsonify({
        "max_steps": config.max_steps,
        "max_time_seconds": config.max_time_seconds,
        "max_recursion_depth": config.max_recursion_depth
    })