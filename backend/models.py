"""
Data models for the execution engine.
Phase 3.2: Execution tracing with primitive-only serialization.
"""
from dataclasses import dataclass

# Hard bounds a client-supplied config can never exceed/go below, regardless
# of what the request asks for. Prevents a single request from requesting an
# effectively unbounded run (huge max_steps/time/recursion/heap) that would
# tie up a worker or exhaust memory. Values are intentionally generous so
# legitimate teaching/demo programs are unaffected.
MIN_STEPS, MAX_STEPS = 1, 200_000
MIN_TIME_SECONDS, MAX_TIME_SECONDS = 0.5, 60.0
MIN_RECURSION_DEPTH, MAX_RECURSION_DEPTH = 1, 2000
MIN_HEAP_OBJECTS, MAX_HEAP_OBJECTS = 1, 100_000
MIN_OUTPUT_CHARS, MAX_OUTPUT_CHARS = 1, 1_000_000


def _clamp(value, low, high, default):
    try:
        value = type(default)(value)
    except (TypeError, ValueError):
        return default
    return max(low, min(high, value))


@dataclass
class ExecutionConfig:
    """Configuration for execution limits."""
    max_steps: int = 10000
    max_time_seconds: float = 30.0
    max_recursion_depth: int = 1000
    max_heap_objects: int = 50000
    max_output_chars: int = 100000

    def __post_init__(self):
        # Clamp (rather than reject) so a slightly-out-of-range client value
        # degrades gracefully to the nearest allowed bound instead of failing
        # the whole request.
        self.max_steps = _clamp(self.max_steps, MIN_STEPS, MAX_STEPS, 10000)
        self.max_time_seconds = _clamp(self.max_time_seconds, MIN_TIME_SECONDS, MAX_TIME_SECONDS, 30.0)
        self.max_recursion_depth = _clamp(self.max_recursion_depth, MIN_RECURSION_DEPTH, MAX_RECURSION_DEPTH, 1000)
        self.max_heap_objects = _clamp(self.max_heap_objects, MIN_HEAP_OBJECTS, MAX_HEAP_OBJECTS, 50000)
        self.max_output_chars = _clamp(self.max_output_chars, MIN_OUTPUT_CHARS, MAX_OUTPUT_CHARS, 100000)
