"""
AST-based code security for the execution engine.

Inspects the user's source code AST to detect forbidden imports,
dangerous function calls, and restricted attribute access.
This is NOT regex-based — it walks the actual Python AST for reliability.
"""

import ast
from typing import Optional
from .errors import SecurityViolationError

# Modules that are forbidden to import
FORBIDDEN_MODULES = {
    "os", "sys", "subprocess", "socket", "http", "httplib",
    "urllib", "requests", "ctypes", "importlib", "signal",
    "multiprocessing", "threading", "shelve", "pickle", "shutil",
    "pathlib", "tempfile", "glob", "fnmatch", "stat",
    "webbrowser", "antigravity", "code", "codeop", "compileall",
    "distutils", "ensurepip", "imaplib", "mailcap", "nis",
    "pdb", "pipes", "poplib", "posix", "posixpath", "profile",
    "pstats", "pty", "pwd", "resource", "smtpd", "smtplib",
    "telnetlib", "uuid", "xmlrpc",
}

# Functions that are forbidden to call
FORBIDDEN_CALLS = {
    "eval", "exec", "compile", "__import__",
    "exit", "quit",
}

# Dangerous attribute accesses
FORBIDDEN_DUNDERS = {
    "__builtins__", "__code__", "__globals__", "__closure__",
    "__subclasses__", "__mro__", "__bases__", "__dict__",
    "__class__", "__init_subclass__", "__setattr__", "__delattr__",
    "__getattribute__", "__reduce__", "__reduce_ex__",
}

# Allow these imports even if they partially match forbidden names
ALLOWED_IMPORTS = {
    "typing", "collections", "functools", "itertools",
    "heapq", "bisect", "math", "random", "string",
    "re", "operator", "copy", "json",
    "dataclasses", "enum", "abc",
    "deque", "Counter", "defaultdict", "OrderedDict",
    "namedtuple", "List", "Dict", "Set", "Tuple", "Optional",
    "Union", "Any", "Callable", "Iterator", "Iterable",
}


def sanitize_source(code: str) -> tuple:
    """
    Inspect source code for security violations using AST analysis.

    Args:
        code: Python source code string.

    Returns:
        (sanitized_code, warnings) tuple where warnings is a list of strings.

    Raises:
        SecurityViolationError: If forbidden constructs are detected.
    """
    warnings = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Don't double-report syntax errors — let the parser handle that
        return code, warnings

    violations = []

    # Check imports
    for node in ast.walk(tree):
        # Import statements
        if isinstance(node, ast.Import):
            for alias in node.names:
                _check_module(alias.name, violations)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            _check_module(module, violations)
            # Also check individual imported names
            for alias in node.names:
                full_name = f"{module}.{alias.name}" if module else alias.name
                if full_name not in ALLOWED_IMPORTS:
                    _check_forbidden_name(alias.name, violations, "import")

        # Function calls
        elif isinstance(node, ast.Call):
            func = node.func
            # Direct name call: eval(), exec(), etc.
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                violations.append(f"Forbidden function call: {func.id}()")
            # Attribute call: os.system(), etc.
            elif isinstance(func, ast.Attribute):
                if func.attr in FORBIDDEN_CALLS:
                    violations.append(f"Forbidden call: ...{func.attr}()")

        # Attribute access on dunder names
        elif isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_DUNDERS:
                violations.append(f"Forbidden attribute access: .{node.attr}")

    if violations:
        message = "Security violations detected:\n• " + "\n• ".join(violations)
        raise SecurityViolationError(message)

    return code, warnings


def _check_module(module_name: str, violations: list):
    """Check if a module name is forbidden."""
    # Check the top-level module
    top_level = module_name.split(".")[0]
    if top_level in FORBIDDEN_MODULES:
        violations.append(f"Forbidden import: {module_name}")
        return

    # Check if any forbidden module is a prefix of the import
    for forbidden in FORBIDDEN_MODULES:
        if module_name.startswith(f"{forbidden}.") or module_name == forbidden:
            violations.append(f"Forbidden import: {module_name}")
            return


def _check_forbidden_name(name: str, violations: list, context: str):
    """Check if a bare name is forbidden."""
    if name in FORBIDDEN_MODULES:
        violations.append(f"Forbidden {context}: {name}")
    if name in FORBIDDEN_DUNDERS:
        violations.append(f"Forbidden {context}: {name}")


def restricted_globals() -> dict:
    """
    Build a restricted __builtins__ dict for use in exec().
    Removes dangerous builtins while keeping the safe ones needed
    for normal algorithm execution.
    """
    import builtins

    # Allowed builtins for algorithm execution
    allowed = {
        "abs", "all", "any", "bin", "bool", "chr", "complex",
        "dict", "divmod", "enumerate", "filter", "float", "format",
        "frozenset", "hash", "hex", "id", "int", "isinstance",
        "issubclass", "iter", "len", "list", "map", "max", "min",
        "next", "oct", "ord", "pow", "print", "range", "repr",
        "reversed", "round", "set", "setattr", "slice", "sorted",
        "str", "sum", "tuple", "type", "zip",
        "True", "False", "None",
        "ValueError", "TypeError", "KeyError", "IndexError",
        "AttributeError", "StopIteration", "RuntimeError",
        "NotImplementedError", "RecursionError",
        "ArithmeticError", "OverflowError", "ZeroDivisionError",
        "AssertionError", "Exception", "BaseException",
        "Exception", "Exception",
    }

    safe_builtins = {}
    for name in allowed:
        try:
            safe_builtins[name] = getattr(builtins, name)
        except AttributeError:
            pass

    return safe_builtins
