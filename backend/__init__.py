"""
Backend package initialization.
"""
from .models import ExecutionConfig
from .tracer import ExecutionTracer, execute_python, Snapshot, serialize_value
from .execution_engine import run_solution, get_registry, list_problems

__all__ = [
    'ExecutionConfig',
    'ExecutionTracer',
    'execute_python',
    'Snapshot',
    'serialize_value',
    'run_solution',
    'get_registry',
    'list_problems',
]