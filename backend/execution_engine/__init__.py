"""
Execution Engine package.
LeetCode-style solution execution with automatic detection,
plugin-based problem registry, and visualization trace generation.

Public API:
    run_solution()   — Execute a LeetCode solution and get test results + trace
    list_problems()  — List all registered problems
    get_registry()   — Access the plugin registry directly
"""

from .runner import run_solution
from .plugin_registry import get_registry

__all__ = [
    "run_solution",
    "get_registry",
]


def list_problems():
    """List all registered problems as plain dicts."""
    return get_registry().list_problem_dicts()
