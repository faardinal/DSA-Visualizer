"""
Backend package initialization.
Phase 3.2: Execution tracing with primitive-only serialization.
"""
from .models import ExecutionConfig
from .tracer import ExecutionTracer, execute_python, Snapshot, serialize_value

__all__ = [
    'ExecutionConfig',
    'ExecutionTracer',
    'execute_python',
    'Snapshot',
    'serialize_value',
]