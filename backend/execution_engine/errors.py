"""
Custom exception hierarchy for the execution engine.
All engine-specific errors inherit from EngineError so callers can
distinguish them from standard Python exceptions.
"""


class EngineError(Exception):
    """Base exception for all execution engine errors."""
    pass


class NoSolutionClassError(EngineError):
    """Raised when the source code does not contain a class named 'Solution'."""
    pass


class NoMethodsError(EngineError):
    """Raised when the Solution class contains no methods."""
    pass


class ParseError(EngineError):
    """Raised when AST parsing of the source code fails."""
    pass


class SecurityViolationError(EngineError):
    """Raised when the source code contains forbidden imports or constructs."""
    pass


class AmbiguousMethodError(EngineError):
    """Raised when a method name matches multiple registered problems."""
    pass


class PluginNotFoundError(EngineError):
    """Raised when no plugin matches the given problem_id."""
    pass


class WrapperGenerationError(EngineError):
    """Raised when wrapper code generation fails."""
    pass


class ResultParseError(EngineError):
    """Raised when parsing the execution result markers fails."""
    pass


# ---------------------------------------------------------------------------
# Error classifier: maps Python exception types to human-readable messages
# and machine-readable categories for the frontend.
# ---------------------------------------------------------------------------

ERROR_CLASSIFICATION = {
    SyntaxError: ("syntax_error", "Syntax Error: {message}"),
    IndentationError: ("syntax_error", "Indentation Error: {message}"),
    ImportError: ("import_error", "Import Error: {message}"),
    ModuleNotFoundError: ("import_error", "Module Not Found: {message}"),
    TypeError: ("runtime_error", "Type Error: {message}"),
    IndexError: ("runtime_error", "Index Error: {message}"),
    KeyError: ("runtime_error", "Key Error: {message}"),
    AttributeError: ("runtime_error", "Attribute Error: {message}"),
    RecursionError: ("recursion_limit", "Recursion Error: Maximum recursion depth exceeded"),
    NameError: ("runtime_error", "Name Error: {message}"),
    ValueError: ("runtime_error", "Value Error: {message}"),
    ZeroDivisionError: ("runtime_error", "Zero Division Error: Division by zero"),
    UnicodeError: ("runtime_error", "Unicode Error: {message}"),
    UnicodeDecodeError: ("runtime_error", "Unicode Decode Error: {message}"),
    UnicodeEncodeError: ("runtime_error", "Unicode Encode Error: {message}"),
    AssertionError: ("wrong_answer", "Assertion Error: {message}"),
    KeyboardInterrupt: ("interrupted", "Execution interrupted"),
    MemoryError: ("memory_limit", "Memory Error: Out of memory"),
    OverflowError: ("runtime_error", "Overflow Error: {message}"),
    StopIteration: ("runtime_error", "Stop Iteration: {message}"),
    RuntimeError: ("runtime_error", "Runtime Error: {message}"),
    NotImplementedError: ("runtime_error", "Not Implemented: {message}"),
    FileNotFoundError: ("runtime_error", "File Not Found: {message}"),
    PermissionError: ("security_violation", "Permission Error: {message}"),
    OSError: ("runtime_error", "OS Error: {message}"),
    TimeoutError: ("time_limit", "Timeout: Execution timed out"),
}


def classify_error(exc: Exception) -> tuple:
    """
    Classify a Python exception into a (error_type, human_message) tuple.

    Returns:
        (str, str): Machine-readable error type and human-readable message.
    """
    exc_type = type(exc)
    # Check exact type first, then MRO for subclasses
    for cls in exc_type.__mro__:
        if cls in ERROR_CLASSIFICATION:
            error_type, template = ERROR_CLASSIFICATION[cls]
            message = template.format(message=str(exc))
            return error_type, message

    # Fallback for unknown exception types
    return "runtime_error", f"{exc_type.__name__}: {exc}"
