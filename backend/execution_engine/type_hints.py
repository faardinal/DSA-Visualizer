"""
Type hint parsing for Python type annotations.
Converts annotation strings into structured TypeHint objects that the
execution engine can use for value generation, serialization, and validation.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TypeHint:
    """
    Structured representation of a Python type annotation.
    Examples:
        int                -> TypeHint(base='int', args=[], is_optional=False, raw='int')
        List[int]          -> TypeHint(base='list', args=[TypeHint(base='int')], ...)
        Optional[str]      -> TypeHint(base='optional', args=[TypeHint(base='str')], is_optional=True, ...)
        TreeNode           -> TypeHint(base='TreeNode', args=[], ...)
    """
    base: str
    args: list = field(default_factory=list)
    is_optional: bool = False
    raw: str = ""

    def __str__(self) -> str:
        if self.is_optional and self.args:
            return f"Optional[{self.args[0]}]"
        if self.args:
            args_str = ", ".join(str(a) for a in self.args)
            return f"{self.base}[{args_str}]"
        return self.base

    def __eq__(self, other):
        if not isinstance(other, TypeHint):
            return False
        return (self.base == other.base
                and self.args == other.args
                and self.is_optional == other.is_optional)

    def __hash__(self):
        return hash((self.base, tuple(self.args), self.is_optional))


# Simple types that don't have type parameters
_PRIMITIVES = {
    "int", "float", "bool", "str", "None", "NoneType",
    "bytes", "bytearray",
}

# Node types that represent data structures
_NODE_TYPES = {
    "TreeNode", "ListNode", "Node", "TrieNode", "GraphNode",
}

# Collection types that have type parameters
_COLLECTION_TYPES = {
    "List", "Tuple", "Set", "FrozenSet", "Dict",
}


def parse_type_hint(annotation_str: str) -> Optional[TypeHint]:
    """
    Parse a type annotation string into a TypeHint.

    Args:
        annotation_str: Python type annotation string, e.g. "List[int]", "Optional[str]"

    Returns:
        TypeHint object, or None if the annotation is empty/unparseable.
    """
    if not annotation_str or not annotation_str.strip():
        return None

    raw = annotation_str.strip()

    # Handle Optional[X] — normalize to Optional wrapper
    if raw.startswith("Optional[") and raw.endswith("]"):
        inner_str = raw[len("Optional["):-1]
        inner = parse_type_hint(inner_str)
        if inner:
            inner.is_optional = True
            inner.raw = raw
            return inner
        return TypeHint(base="optional", args=[TypeHint(base=inner_str.strip())],
                        is_optional=True, raw=raw)

    # Handle Union[X, None] (equivalent to Optional[X])
    if raw.startswith("Union[") and raw.endswith("]"):
        inner_str = raw[len("Union["):-1]
        # Split by ", " but handle nested brackets
        parts = _split_type_args(inner_str)
        non_none = [p.strip() for p in parts if p.strip() not in ("None", "NoneType")]
        if len(non_none) == 1:
            return parse_type_hint(f"Optional[{non_none[0]}]")
        # Multi-type union — treat the first non-None as the primary type
        if non_none:
            primary = parse_type_hint(non_none[0])
            if primary:
                primary.is_optional = True
                primary.raw = raw
                return primary

    # Handle collection types: List[int], Dict[str, int], Tuple[int, str]
    for coll_type in _COLLECTION_TYPES:
        if raw.startswith(f"{coll_type}[") and raw.endswith("]"):
            inner_str = raw[len(coll_type) + 1:-1]
            arg_strs = _split_type_args(inner_str)
            args = [parse_type_hint(a.strip()) or TypeHint(base=a.strip()) for a in arg_strs]
            base = coll_type.lower()  # Normalize: "List" -> "list"
            return TypeHint(base=base, args=args, raw=raw)

    # Handle plain types
    stripped = raw.strip()
    return TypeHint(base=stripped, raw=stripped)


def _split_type_args(s: str) -> list:
    """
    Split type arguments by comma, respecting nested brackets.
    E.g. "int, List[str]" -> ["int", "List[str]"]
         "Dict[str, List[int]]" -> ["str", "List[int]"]
    """
    parts = []
    depth = 0
    current = []
    for ch in s:
        if ch in ("[", "("):
            depth += 1
            current.append(ch)
        elif ch in ("]", ")"):
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current))
    return parts


def type_hint_to_python(th: TypeHint) -> str:
    """Convert a TypeHint back to a Python type annotation string."""
    if th.raw:
        return th.raw
    if th.args:
        args_str = ", ".join(type_hint_to_python(a) for a in th.args)
        return f"{th.base}[{args_str}]"
    return th.base


def is_serializable(th: TypeHint) -> bool:
    """
    Check if a type can be directly JSON-serialized without custom builders.
    Primitives and collections of primitives are serializable.
    Node types (TreeNode, ListNode) require builders.
    """
    if th.base in _PRIMITIVES:
        return True
    if th.base in _NODE_TYPES:
        return False
    if th.base in ("list", "tuple", "set", "frozenset", "dict"):
        return all(is_serializable(a) for a in th.args)
    return th.base not in _NODE_TYPES


def is_node_type(th: TypeHint) -> bool:
    """Check if a type hint represents a data structure node."""
    if th.base in _NODE_TYPES:
        return True
    if th.is_optional and th.args:
        return is_node_type(th.args[0])
    return False


def is_collection_type(th: TypeHint) -> bool:
    """Check if a type hint represents a collection."""
    return th.base in ("list", "tuple", "set", "frozenset", "dict")
