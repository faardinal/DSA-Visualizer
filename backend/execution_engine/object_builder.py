"""
Data structure builders and serializers for the execution engine.

Converts JSON-like test data into Python objects (ListNode, TreeNode, etc.)
and serializes them back for comparison. All functions are pure and testable.

These classes and functions are injected into generated wrapper code so that
user solutions can operate on proper data structures, not raw lists.
"""


# ---------------------------------------------------------------------------
# ListNode (singly-linked list) — LeetCode-compatible
# ---------------------------------------------------------------------------

class ListNode:
    """Singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode(val={self.val})"

    def __eq__(self, other):
        if not isinstance(other, ListNode):
            return False
        return self.val == other.val and self.next == other.next


def build_linked_list(items: list) -> ListNode:
    """
    Build a singly-linked list from a Python list.
    E.g. [1, 2, 3] -> 1 -> 2 -> 3 -> None
    """
    if not items:
        return None

    dummy = ListNode(0)
    current = dummy
    for item in items:
        current.next = ListNode(item)
        current = current.next
    return dummy.next


def serialize_linked_list(head: ListNode) -> list:
    """
    Serialize a linked list back to a Python list.
    Handles cycles by stopping at 5000 nodes.
    """
    result = []
    visited = set()
    current = head
    while current is not None:
        node_id = id(current)
        if node_id in visited:
            result.append(f"cycle_at_{current.val}")
            break
        visited.add(node_id)
        result.append(current.val)
        current = current.next
        if len(result) > 5000:
            break
    return result


def linked_list_to_array(head: ListNode) -> list:
    """Alias for serialize_linked_list — more descriptive name for wrappers."""
    return serialize_linked_list(head)


# ---------------------------------------------------------------------------
# TreeNode (binary tree) — LeetCode-compatible
# ---------------------------------------------------------------------------

class TreeNode:
    """Binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode(val={self.val})"

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return (self.val == other.val
                and self.left == other.left
                and self.right == other.right)


def build_binary_tree(items: list) -> TreeNode:
    """
    Build a binary tree from a level-order list (LeetCode format).
    None values represent missing nodes.
    E.g. [1, 2, 3, null, 4] ->
         1
        / \\
       2   3
        \\
         4
    """
    if not items:
        return None

    root = TreeNode(items[0])
    queue = [root]
    i = 1

    while queue and i < len(items):
        node = queue.pop(0)

        if i < len(items) and items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1

        if i < len(items) and items[i] is not None:
            node.right = TreeNode(items[i])
            queue.append(node.right)
        i += 1

    return root


def serialize_binary_tree(root: TreeNode) -> list:
    """
    Serialize a binary tree to a level-order list with nulls.
    Trailing nulls are stripped.
    """
    if root is None:
        return []

    result = []
    queue = [root]

    while queue:
        node = queue.pop(0)

        if node is None:
            result.append(None)
            continue

        result.append(node.val)
        queue.append(node.left)
        queue.append(node.right)

    # Strip trailing nulls
    while result and result[-1] is None:
        result.pop()

    return result


def tree_to_array(root: TreeNode) -> list:
    """Alias for serialize_binary_tree."""
    return serialize_binary_tree(root)


# ---------------------------------------------------------------------------
# TrieNode
# ---------------------------------------------------------------------------

class TrieNode:
    """Trie (prefix tree) node."""
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.val = ""

    def __repr__(self):
        return f"TrieNode(end={self.is_end}, children={list(self.children.keys())})"


def build_trie(words: list) -> TrieNode:
    """Build a trie from a list of words."""
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
        node.val = word
    return root


def serialize_trie(root: TrieNode) -> list:
    """Serialize a trie back to a list of words via DFS."""
    if root is None:
        return []
    words = []
    _collect_words(root, "")
    return words


def _collect_words(node: TrieNode, prefix: str, words: list = None):
    """DFS to collect all words in a trie."""
    if words is None:
        words = []
    if node.is_end:
        words.append(prefix or node.val)
    for ch, child in sorted(node.children.items()):
        _collect_words(child, prefix + ch, words)
    return words


# ---------------------------------------------------------------------------
# Graph utilities
# ---------------------------------------------------------------------------

def build_graph(n: int, edges: list) -> dict:
    """
    Build an adjacency list representation of a graph.
    Args:
        n: Number of nodes (0 to n-1).
        edges: List of [u, v] pairs (undirected).
    Returns:
        dict: {node: [neighbors]}
    """
    graph = {i: [] for i in range(n)}
    for edge in edges:
        if len(edge) >= 2:
            u, v = edge[0], edge[1]
            if u in graph:
                graph[u].append(v)
            if v in graph:
                graph[v].append(u)
    return graph


def build_directed_graph(n: int, edges: list) -> dict:
    """
    Build a directed adjacency list representation of a graph.
    """
    graph = {i: [] for i in range(n)}
    for edge in edges:
        if len(edge) >= 2:
            u, v = edge[0], edge[1]
            if u in graph:
                graph[u].append(v)
    return graph


def serialize_graph(graph: dict) -> list:
    """Serialize adjacency list to a sorted list of [node, [neighbors]] pairs."""
    if not graph:
        return []
    result = []
    for node in sorted(graph.keys()):
        result.append([node, sorted(graph[node])])
    return result


# ---------------------------------------------------------------------------
# Generic build dispatcher (used by wrapper generator)
# ---------------------------------------------------------------------------

def build_value(type_name: str, raw_value):
    """
    Build a Python object from raw JSON-like value based on type name.
    Used by wrapper templates to convert test data into proper objects.
    """
    if raw_value is None:
        return None

    if type_name == "ListNode":
        if isinstance(raw_value, list):
            return build_linked_list(raw_value)
        return raw_value

    if type_name == "TreeNode":
        if isinstance(raw_value, list):
            return build_binary_tree(raw_value)
        return raw_value

    if type_name == "TrieNode":
        if isinstance(raw_value, list):
            return build_trie(raw_value)
        return raw_value

    return raw_value


def serialize_result(result, result_type: str = "auto"):
    """
    Serialize a result back to JSON-safe form for stdout capture.
    Used by wrapper templates to convert result objects back to lists.
    """
    if result is None:
        return None

    if result_type == "auto" or result_type == "":
        # Auto-detect
        if isinstance(result, ListNode):
            return serialize_linked_list(result)
        if isinstance(result, TreeNode):
            return serialize_binary_tree(result)
        if isinstance(result, TrieNode):
            return serialize_trie(result)

    return result


# ---------------------------------------------------------------------------
# Helper code strings for injection into wrapper templates
# ---------------------------------------------------------------------------

LIST_NODE_HELPERS = '''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        return f"ListNode(val={self.val})"

def build_linked_list(items):
    if not items:
        return None
    dummy = ListNode(0)
    current = dummy
    for item in items:
        current.next = ListNode(item)
        current = current.next
    return dummy.next

def serialize_linked_list(head):
    result = []
    visited = set()
    current = head
    while current is not None:
        nid = id(current)
        if nid in visited:
            break
        visited.add(nid)
        result.append(current.val)
        current = current.next
        if len(result) > 5000:
            break
    return result
'''

TREE_NODE_HELPERS = '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        return f"TreeNode(val={self.val})"

def build_binary_tree(items):
    if not items:
        return None
    from collections import deque
    root = TreeNode(items[0])
    queue = deque([root])
    i = 1
    while queue and i < len(items):
        node = queue.popleft()
        if i < len(items) and items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items) and items[i] is not None:
            node.right = TreeNode(items[i])
            queue.append(node.right)
        i += 1
    return root

def serialize_binary_tree(root):
    if root is None:
        return []
    result = []
    from collections import deque
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
            continue
        result.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while result and result[-1] is None:
        result.pop()
    return result
'''

GRAPH_HELPERS = '''
def build_graph(n, edges):
    graph = {i: [] for i in range(n)}
    for edge in edges:
        if len(edge) >= 2:
            u, v = edge[0], edge[1]
            if u in graph:
                graph[u].append(v)
            if v in graph:
                graph[v].append(u)
    return graph

def build_directed_graph(n, edges):
    graph = {i: [] for i in range(n)}
    for edge in edges:
        if len(edge) >= 2:
            u, v = edge[0], edge[1]
            if u in graph:
                graph[u].append(v)
    return graph

def serialize_graph(graph):
    if not graph:
        return []
    result = []
    for node in sorted(graph.keys()):
        result.append([node, sorted(graph[node])])
    return result
'''
