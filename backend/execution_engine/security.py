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
    "eval", "exec", "compile", "__import__", "open", "input",
    "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr",
    "breakpoint", "help", "exit", "quit",
}

# Dangerous attribute accesses
FORBIDDEN_DUNDERS = {
    "__builtins__", "__code__", "__globals__", "__closure__",
    "__subclasses__", "__mro__", "__bases__", "__dict__",
    "__class__", "__init_subclass__", "__setattr__", "__delattr__",
    "__getattribute__", "__reduce__", "__reduce_ex__",
}

FORBIDDEN_ATTRIBUTES = FORBIDDEN_DUNDERS | {
    "mro", "register", "__call__", "__new__", "__del__",
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

        # Bare-name references to dangerous dunders (e.g. `__builtins__`).
        # Reading these as plain names is not caught by the attribute/dot-access
        # rule below, yet hands the user a handle to restricted runtime objects.
        # No legitimate LeetCode solution ever reads these names, so blocking
        # the bare reference is safe and closes a defense-in-depth gap.
        elif isinstance(node, ast.Name):
            if node.id in FORBIDDEN_DUNDERS:
                violations.append(f"Forbidden name reference: {node.id}")

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
            if node.attr in FORBIDDEN_ATTRIBUTES:
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
    if name.startswith("__") and name.endswith("__"):
        violations.append(f"Forbidden {context}: {name}")
