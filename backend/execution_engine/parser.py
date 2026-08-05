"""
AST-based parser for LeetCode-style Solution classes.
Extracts the class definition, method signatures, parameter names,
type annotations, and decorators from Python source code.
"""

import ast
from dataclasses import dataclass, field
from typing import Optional

from .type_hints import TypeHint, parse_type_hint
from .errors import NoSolutionClassError, NoMethodsError, ParseError


@dataclass
class ParamInfo:
    """Information about a single method parameter."""
    name: str
    annotation: Optional[TypeHint] = None
    annotation_str: str = ""


@dataclass
class MethodInfo:
    """Information about a single method in the Solution class."""
    name: str
    params: list = field(default_factory=list)  # List[ParamInfo]
    return_annotation: Optional[TypeHint] = None
    return_annotation_str: str = ""
    is_static: bool = False
    decorators: list = field(default_factory=list)  # List[str]


@dataclass
class ParsedSolution:
    """Result of parsing a Solution class from source code."""
    class_name: str
    methods: list = field(default_factory=list)  # List[MethodInfo]
    imports: list = field(default_factory=list)   # List[str] — import statements found


def parse_source(code: str) -> ParsedSolution:
    """
    Parse Python source code and extract the Solution class definition.

    Args:
        code: Python source code string.

    Returns:
        ParsedSolution with class name, methods, parameters, and type annotations.

    Raises:
        ParseError: If the source code has syntax errors.
        NoSolutionClassError: If no class named 'Solution' is found.
        NoMethodsError: If the Solution class has no methods.
    """
    # Try to parse the AST
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ParseError(f"Syntax error at line {e.lineno}: {e.msg}")

    # Extract import statements
    imports = _extract_imports(tree)

    # Find the Solution class
    solution_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Solution":
            solution_class = node
            break

    if solution_class is None:
        raise NoSolutionClassError(
            "No 'class Solution' found in the source code. "
            "Please define a Solution class with your method."
        )

    # Extract methods
    methods = []
    for item in solution_class.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            method = _parse_method(item)
            if method:
                methods.append(method)

    if not methods:
        raise NoMethodsError(
            "The Solution class contains no methods. "
            "Please add at least one method."
        )

    return ParsedSolution(
        class_name=solution_class.name,
        methods=methods,
        imports=imports,
    )


def _extract_imports(tree: ast.Module) -> list:
    """Extract import statement strings from the AST."""
    imports = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")
    return imports


def _parse_method(node) -> Optional[MethodInfo]:
    """
    Parse an ast.FunctionDef into a MethodInfo.
    Skips dunder methods (__init__, __str__, etc.) and private methods (_foo).
    """
    name = node.name

    # Skip dunder and private methods
    if name.startswith("__") and name.endswith("__"):
        return None
    if name.startswith("_"):
        return None

    # Detect decorators
    decorators = []
    is_static = False
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "staticmethod":
            is_static = True
            decorators.append("staticmethod")
        elif isinstance(dec, ast.Attribute) and dec.attr == "staticmethod":
            is_static = True
            decorators.append("staticmethod")
        elif isinstance(dec, ast.Name):
            decorators.append(dec.id)
        elif isinstance(dec, ast.Attribute):
            decorators.append(dec.attr)
        else:
            decorators.append("decorator")

    # Extract parameters (skip 'self' and 'cls')
    params = []
    args = node.args

    # Determine which args to skip
    skip_names = {"self", "cls"}
    all_args = args.args + args.posonlyargs + args.kwonlyargs

    for arg in all_args:
        if arg.arg in skip_names:
            continue

        annotation_str = ""
        annotation = None
        if arg.annotation:
            annotation_str = ast.unparse(arg.annotation)
            try:
                annotation = parse_type_hint(annotation_str)
            except Exception:
                annotation = None

        params.append(ParamInfo(
            name=arg.arg,
            annotation=annotation,
            annotation_str=annotation_str,
        ))

    # Extract return annotation
    return_annotation = None
    return_annotation_str = ""
    if node.returns:
        return_annotation_str = ast.unparse(node.returns)
        try:
            return_annotation = parse_type_hint(return_annotation_str)
        except Exception:
            return_annotation = None

    return MethodInfo(
        name=name,
        params=params,
        return_annotation=return_annotation,
        return_annotation_str=return_annotation_str,
        is_static=is_static,
        decorators=decorators,
    )


def has_solution_class(code: str) -> bool:
    """Quick check: does the source code contain 'class Solution'?"""
    return "class Solution" in code or "class Solution:" in code or "class Solution(" in code
