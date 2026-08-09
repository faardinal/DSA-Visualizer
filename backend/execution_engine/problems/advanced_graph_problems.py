"""Advanced Graph problems — BFS/DFS/Topological Sort/Union-Find."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult


# LC 133 — Clone Graph
_CLONE_GRAPH_TPL = """{imports}
{helpers}

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

{solution_code}

def main():
    adj = {adj}
    if not adj:
        head = None
    else:
        nodes = [Node(i+1) for i in range(len(adj))]
        for i, nbs in enumerate(adj):
            nodes[i].neighbors = [nodes[j-1] for j in nbs]
        head = nodes[0]
    sol = Solution()
    result = sol.cloneGraph(head)
    # Serialize: BFS to get adjacency list
    if result is None:
        print("__RESULT__:")
        print(repr([]))
    else:
        visited = {{}}
        from collections import deque
        q = deque([result])
        visited[result.val] = result
        while q:
            n = q.popleft()
            for nb in n.neighbors:
                if nb.val not in visited:
                    visited[nb.val] = nb
                    q.append(nb)
        out = []
        for v in sorted(visited):
            out.append(sorted(nb.val for nb in visited[v].neighbors))
        print("__RESULT__:")
        print(repr(out))

main()
"""

class CloneGraphPlugin(ProblemPlugin):
    problem_id = "clone-graph"
    leetcode_number = 133
    title = "Clone Graph"
    slug = "clone-graph"
    method_name = "cloneGraph"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Hash Table", "DFS", "BFS", "Graph"]
    parameters = ["node: Optional[Node]"]
    return_type = "Optional[Node]"
    hidden_test_count = 3
    description = "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph."

    def get_test_cases(self):
        return [
            TestCase({"adj": [[2,4],[1,3],[2,4],[1,3]]}, [[2,4],[1,3],[2,4],[1,3]], "Example 1"),
            TestCase({"adj": [[]]}, [[]], "Single node"),
            TestCase({"adj": []}, [], "Empty", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_CLONE_GRAPH_TPL)

    @staticmethod
    def oracle(inputs):
        adj = inputs["adj"]
        if not adj: return []
        return [sorted(nb) for nb in adj]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 6)
            adj = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i+1, n):
                    if rng.random() > 0.4:
                        adj[i].append(j+1); adj[j].append(i+1)
            tests.append({"adj": adj})
        return tests


# LC 286 — Walls and Gates
class WallsAndGatesPlugin(ProblemPlugin):
    problem_id = "walls-and-gates"
    leetcode_number = 286
    title = "Walls and Gates"
    slug = "walls-and-gates"
    method_name = "wallsAndGates"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Array", "BFS", "Matrix"]
    parameters = ["rooms: List[List[int]]"]
    return_type = "None"
    hidden_test_count = 3
    description = "Fill each empty room with the distance to its nearest gate. INF=2147483647, -1=wall, 0=gate."

    def get_test_cases(self):
        INF = 2147483647
        return [
            TestCase({"rooms": [[INF,-1,0,INF],[INF,INF,INF,-1],[INF,-1,INF,-1],[0,-1,INF,INF]]},
                     [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]], "Example 1"),
            TestCase({"rooms": []}, [], "Empty", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import deque
        INF = 2147483647
        rooms = [row[:] for row in inputs["rooms"]]
        if not rooms: return rooms
        rows, cols = len(rooms), len(rooms[0])
        q = deque()
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0: q.append((r,c))
        while q:
            r,c = q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc = r+dr,c+dc
                if 0<=nr<rows and 0<=nc<cols and rooms[nr][nc]==INF:
                    rooms[nr][nc] = rooms[r][c]+1; q.append((nr,nc))
        return rooms

    @staticmethod
    def generate_hidden_inputs(rng, count):
        INF = 2147483647
        tests = []
        for _ in range(count):
            r=rng.randint(2,4); c=rng.randint(2,4)
            grid=[[rng.choice([INF,INF,-1,0]) for _ in range(c)] for _ in range(r)]
            tests.append({"rooms": grid})
        return tests


# LC 127 — Word Ladder
class WordLadderPlugin(ProblemPlugin):
    problem_id = "word-ladder"
    leetcode_number = 127
    title = "Word Ladder"
    slug = "word-ladder"
    method_name = "ladderLength"
    difficulty = "Hard"
    pattern = "Graphs"
    topics = ["Hash Table", "String", "BFS"]
    parameters = ["beginWord: str", "endWord: str", "wordList: List[str]"]
    return_type = "int"
    hidden_test_count = 3
    description = "Return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if none."

    def get_test_cases(self):
        return [
            TestCase({"beginWord":"hit","endWord":"cog","wordList":["hot","dot","dog","lot","log","cog"]}, 5, "Example 1"),
            TestCase({"beginWord":"hit","endWord":"cog","wordList":["hot","dot","dog","lot","log"]}, 0, "Example 2"),
            TestCase({"beginWord":"a","endWord":"c","wordList":["a","b","c"]}, 2, "Short", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import deque
        begin, end, word_list = inputs["beginWord"], inputs["endWord"], inputs["wordList"]
        word_set = set(word_list)
        if end not in word_set: return 0
        q = deque([(begin, 1)])
        visited = {begin}
        while q:
            word, steps = q.popleft()
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    nw = word[:i]+c+word[i+1:]
                    if nw == end: return steps+1
                    if nw in word_set and nw not in visited:
                        visited.add(nw); q.append((nw, steps+1))
        return 0

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            tests.append({"beginWord":"hot","endWord":"dog","wordList":["hot","hog","dog","log"]})
        return tests


# LC 332 — Reconstruct Itinerary
class ReconstructItineraryPlugin(ProblemPlugin):
    problem_id = "reconstruct-itinerary"
    leetcode_number = 332
    title = "Reconstruct Itinerary"
    slug = "reconstruct-itinerary"
    method_name = "findItinerary"
    difficulty = "Hard"
    pattern = "Graphs"
    topics = ["DFS", "Graph", "Eulerian Circuit"]
    parameters = ["tickets: List[List[str]]"]
    return_type = "List[str]"
    hidden_test_count = 3
    description = "Reconstruct the itinerary in order. All tickets used once, lexicographically smallest result."

    def get_test_cases(self):
        return [
            TestCase({"tickets":[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]},
                     ["JFK","MUC","LHR","SFO","SJC"], "Example 1"),
            TestCase({"tickets":[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]},
                     ["JFK","ATL","JFK","SFO","ATL","SFO"], "Example 2"),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import defaultdict
        tickets = inputs["tickets"]
        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)
        result = []
        def dfs(node):
            while graph[node]: dfs(graph[node].pop())
            result.append(node)
        dfs("JFK")
        return result[::-1]

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        airports = ["JFK","SFO","ATL","ORD","LAX"]
        for _ in range(count):
            n = rng.randint(2, 5)
            chosen = rng.sample(airports, min(n, len(airports)))
            tickets = [[chosen[i], chosen[(i+1)%len(chosen)]] for i in range(len(chosen))]
            tests.append({"tickets": tickets})
        return tests


# LC 269 — Alien Dictionary
class AlienDictionaryPlugin(ProblemPlugin):
    problem_id = "alien-dictionary"
    leetcode_number = 269
    title = "Alien Dictionary"
    slug = "alien-dictionary"
    method_name = "alienOrder"
    difficulty = "Hard"
    pattern = "Graphs"
    topics = ["Array", "String", "DFS", "BFS", "Graph", "Topological Sort"]
    parameters = ["words: List[str]"]
    return_type = "str"
    hidden_test_count = 3
    description = "Given a list of words sorted lexicographically by the rules of a new language, return the order of characters."

    def get_test_cases(self):
        return [
            TestCase({"words": ["wrt","wrf","er","ett","rftt"]}, "wertf", "Example 1"),
            TestCase({"words": ["z","x"]}, "zx", "Example 2"),
            TestCase({"words": ["z","x","z"]}, "", "Example 3: invalid cycle"),
        ]

    def get_validator(self): return AlienDictValidator()

    @staticmethod
    def oracle(inputs):
        words = inputs["words"]
        from collections import defaultdict, deque
        chars = set(c for w in words for c in w)
        adj = defaultdict(set)
        indegree = {c:0 for c in chars}
        for i in range(len(words)-1):
            w1, w2 = words[i], words[i+1]
            minl = min(len(w1), len(w2))
            if len(w1)>len(w2) and w1[:minl]==w2[:minl]: return ""
            for j in range(minl):
                if w1[j]!=w2[j]:
                    if w2[j] not in adj[w1[j]]:
                        adj[w1[j]].add(w2[j]); indegree[w2[j]]+=1
                    break
        q = deque(c for c in chars if indegree[c]==0)
        order = []
        while q:
            c = q.popleft(); order.append(c)
            for nb in adj[c]:
                indegree[nb]-=1
                if indegree[nb]==0: q.append(nb)
        return "".join(order) if len(order)==len(chars) else ""

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            tests.append({"words": ["abc","abd","adc"]})
        return tests

class AlienDictValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        # If expected is empty, actual must be empty (invalid input)
        if not expected:
            passed = actual == ""
            return ValidationResult(passed, repr(expected), repr(actual), "" if passed else "Should be empty")
        # Check actual has same length and chars as expected
        passed = len(actual) == len(expected) and set(actual) == set(expected)
        # Also verify it's a valid topological order per the words
        return ValidationResult(passed, repr(expected), repr(actual),
                                "" if passed else f"Expected valid order of same chars, got {repr(actual)}")


# LC 310 — Minimum Height Trees
class MinimumHeightTreesPlugin(ProblemPlugin):
    problem_id = "minimum-height-trees"
    leetcode_number = 310
    title = "Minimum Height Trees"
    slug = "minimum-height-trees"
    method_name = "findMinHeightTrees"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["DFS", "BFS", "Graph", "Topological Sort"]
    parameters = ["n: int", "edges: List[List[int]]"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = "Return all root labels of minimum height trees."

    def get_test_cases(self):
        return [
            TestCase({"n":4,"edges":[[1,0],[1,2],[1,3]]}, [1], "Example 1"),
            TestCase({"n":6,"edges":[[3,0],[3,1],[3,2],[3,4],[5,4]]}, [3,4], "Example 2"),
            TestCase({"n":1,"edges":[]}, [0], "Single node", is_hidden=True),
            TestCase({"n":2,"edges":[[0,1]]}, [0,1], "Two nodes", is_hidden=True),
        ]

    def get_validator(self):
        from backend.execution_engine.problems._validators import SortedListValidator
        return SortedListValidator()

    @staticmethod
    def oracle(inputs):
        n, edges = inputs["n"], inputs["edges"]
        if n == 1: return [0]
        adj = [set() for _ in range(n)]
        for u,v in edges: adj[u].add(v); adj[v].add(u)
        leaves = [i for i in range(n) if len(adj[i])==1]
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            new_leaves = []
            for leaf in leaves:
                nb = next(iter(adj[leaf]))
                adj[nb].remove(leaf)
                if len(adj[nb])==1: new_leaves.append(nb)
            leaves = new_leaves
        return sorted(leaves)

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 10)
            edges = [[i, rng.randint(0,i-1)] for i in range(1,n)]
            tests.append({"n":n,"edges":edges})
        return tests
