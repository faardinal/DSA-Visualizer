"""
Flask routes for the execution API.
"""
from flask import Blueprint, request, jsonify
import time

# Use absolute imports so this module works both when run directly
# and when imported by gunicorn as part of the backend package.
from backend.tracer import execute_python
from backend.models import ExecutionConfig

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
    """Execute Python code and return execution trace."""
    start_time = time.time()

    try:
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({
                "success": False,
                "trace": [],
                "error": "Invalid JSON request",
                "error_type": "invalid_request"
            }), 400

        code = data.get('code', '')
        if not code or not isinstance(code, str):
            return jsonify({
                "success": False,
                "trace": [],
                "error": "No code provided",
                "error_type": "invalid_request"
            }), 400

        inputs = data.get('inputs', '')
        if not isinstance(inputs, str):
            return jsonify({
                "success": False,
                "trace": [],
                "error": "'inputs' must be a string",
                "error_type": "invalid_request"
            }), 400

        config_data = data.get('config') or {}
        if not isinstance(config_data, dict):
            config_data = {}
        config = ExecutionConfig(
            max_steps=config_data.get('max_steps', 10000),
            max_time_seconds=config_data.get('max_time_seconds', 30.0),
            max_recursion_depth=config_data.get('max_recursion_depth', 1000)
        )

        snapshots, error, exec_time, error_type = execute_python(code, inputs, config)
        trace = [snapshot_to_dict(s) for s in snapshots]

        if error:
            response = {
                "success": False,
                "trace": trace,
                "error": error,
                "error_type": error_type or "runtime_error",
                "execution_time": exec_time
            }
        else:
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
    return jsonify({"status": "ok"})


@execution_bp.route('/config', methods=['GET'])
def get_config():
    config = ExecutionConfig()
    return jsonify({
        "max_steps": config.max_steps,
        "max_time_seconds": config.max_time_seconds,
        "max_recursion_depth": config.max_recursion_depth
    })
