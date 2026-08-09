"""Graph / BFS / DFS / Union-Find pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult


# ═══════════════════════════════════════════════════════════════════════════
# LC 695 — Max Area of Island
# ═══════════════════════════════════════════════════════════════════════════
class MaxAreaOfIslandPlugin(ProblemPlugin):
    problem_id = "max-area-of-island"
    leetcode_number = 695
    title = "Max Area of Island"
    slug = "max-area-of-island"
    method_name = "maxAreaOfIsland"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Array", "DFS", "BFS", "Union Find", "Matrix"]
    parameters = ["grid: List[List[int]]"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given a binary 2D grid, return the maximum area of an island (group of connected 1s)."

    def get_test_cases(self):
        return [
            TestCase({"grid": [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],
                [0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],
                [0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]}, 6, "Example 1"),
            TestCase({"grid": [[0,0,0,0,0,0,0,0]]}, 0, "No island"),
            TestCase({"grid": [[1,1],[1,1]]}, 4, "2x2 island", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        grid = [row[:] for row in inputs["grid"]]
        rows, cols = len(grid), len(grid[0]) if grid else 0
        best = 0
        def dfs(r, c):
            if r<0 or r>=rows or c<0 or c>=cols or grid[r][c]==0: return 0
            grid[r][c] = 0
            return 1+dfs(r+1,c)+dfs(r-1,c)+dfs(r,c+1)+dfs(r,c-1)
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]==1: best=max(best,dfs(r,c))
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            rows=rng.randint(2,6); cols=rng.randint(2,6)
            grid=[[rng.randint(0,1) for _ in range(cols)] for _ in range(rows)]
            tests.append({"grid":grid})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 417 — Pacific Atlantic Water Flow
# ═══════════════════════════════════════════════════════════════════════════
class PacificAtlanticPlugin(ProblemPlugin):
    problem_id = "pacific-atlantic-water-flow"
    leetcode_number = 417
    title = "Pacific Atlantic Water Flow"
    slug = "pacific-atlantic-water-flow"
    method_name = "pacificAtlantic"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Array", "DFS", "BFS", "Matrix"]
    parameters = ["heights: List[List[int]]"]
    return_type = "List[List[int]]"
    hidden_test_count = 3
    description = "Return all grid cells from which water can flow to both the Pacific and Atlantic ocean."

    def get_test_cases(self):
        return [
            TestCase({"heights": [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]},
                     [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]], "Example 1"),
            TestCase({"heights": [[1]]}, [[0,0]], "1x1"),
        ]

    def get_validator(self): return AnyOrderPairValidator()

    @staticmethod
    def oracle(inputs):
        matrix = inputs["heights"]
        if not matrix: return []
        rows, cols = len(matrix), len(matrix[0])
        def bfs(starts):
            from collections import deque
            visited = set(starts)
            q = deque(starts)
            while q:
                r,c = q.popleft()
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visited and matrix[nr][nc]>=matrix[r][c]:
                        visited.add((nr,nc)); q.append((nr,nc))
            return visited
        pac = bfs([(0,c) for c in range(cols)]+[(r,0) for r in range(rows)])
        atl = bfs([(rows-1,c) for c in range(cols)]+[(r,cols-1) for r in range(rows)])
        return sorted([r,c] for r,c in pac&atl)

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            r=rng.randint(2,5); c=rng.randint(2,5)
            tests.append({"heights":[[rng.randint(1,20) for _ in range(c)] for _ in range(r)]})
        return tests

class AnyOrderPairValidator(Validator):
    def validate(self, actual, expected, inputs=None):
        try:
            a=sorted(tuple(p) for p in actual); e=sorted(tuple(p) for p in expected)
            passed=a==e
        except Exception: passed=False; a=actual; e=expected
        return ValidationResult(passed,repr(e),repr(a),"" if passed else "Pairs differ")


# ═══════════════════════════════════════════════════════════════════════════
# LC 130 — Surrounded Regions
# ═══════════════════════════════════════════════════════════════════════════
class SurroundedRegionsPlugin(ProblemPlugin):
    problem_id = "surrounded-regions"
    leetcode_number = 130
    title = "Surrounded Regions"
    slug = "surrounded-regions"
    method_name = "solve"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Array", "DFS", "BFS", "Union Find", "Matrix"]
    parameters = ["board: List[List[str]]"]
    return_type = "None"
    hidden_test_count = 4
    description = "Capture all regions surrounded by 'X'. An 'O' is captured if surrounded on all 4 sides by 'X'."

    def get_test_cases(self):
        return [
            TestCase({"board":[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]},
                     [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]], "Example 1"),
            TestCase({"board":[["X"]]}, [["X"]], "1x1"),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        board = [row[:] for row in inputs["board"]]
        if not board: return board
        rows, cols = len(board), len(board[0])
        def dfs(r, c):
            if r<0 or r>=rows or c<0 or c>=cols or board[r][c]!='O': return
            board[r][c]='S'
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]: dfs(r+dr,c+dc)
        for r in range(rows):
            if board[r][0]=='O': dfs(r,0)
            if board[r][cols-1]=='O': dfs(r,cols-1)
        for c in range(cols):
            if board[0][c]=='O': dfs(0,c)
            if board[rows-1][c]=='O': dfs(rows-1,c)
        for r in range(rows):
            for c in range(cols):
                if board[r][c]=='O': board[r][c]='X'
                elif board[r][c]=='S': board[r][c]='O'
        return board

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            r=rng.randint(2,5); c=rng.randint(2,5)
            board=[['X' if rng.random()>0.35 else 'O' for _ in range(c)] for _ in range(r)]
            tests.append({"board":board})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 994 — Rotting Oranges
# ═══════════════════════════════════════════════════════════════════════════
class RottingOrangesPlugin(ProblemPlugin):
    problem_id = "rotting-oranges"
    leetcode_number = 994
    title = "Rotting Oranges"
    slug = "rotting-oranges"
    method_name = "orangesRotting"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Array", "BFS", "Matrix"]
    parameters = ["grid: List[List[int]]"]
    return_type = "int"
    hidden_test_count = 4
    description = "Return the minimum number of minutes to rot all oranges, or -1 if impossible."

    def get_test_cases(self):
        return [
            TestCase({"grid": [[2,1,1],[1,1,0],[0,1,1]]}, 4, "Example 1"),
            TestCase({"grid": [[2,1,1],[0,1,1],[1,0,1]]}, -1, "Example 2: impossible"),
            TestCase({"grid": [[0,2]]}, 0, "Example 3"),
            TestCase({"grid": [[1,2]]}, 1, "One step", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import deque
        grid = [row[:] for row in inputs["grid"]]
        rows,cols = len(grid),len(grid[0])
        q = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]==2: q.append((r,c,0))
                elif grid[r][c]==1: fresh+=1
        minutes=0
        while q:
            r,c,t=q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1:
                    grid[nr][nc]=2; fresh-=1; minutes=t+1; q.append((nr,nc,t+1))
        return minutes if fresh==0 else -1

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            r=rng.randint(2,5); c=rng.randint(2,5)
            grid=[[rng.choice([0,1,1,2]) for _ in range(c)] for _ in range(r)]
            tests.append({"grid":grid})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 207 — Course Schedule
# ═══════════════════════════════════════════════════════════════════════════
class CourseSchedulePlugin(ProblemPlugin):
    problem_id = "course-schedule"
    leetcode_number = 207
    title = "Course Schedule"
    slug = "course-schedule"
    method_name = "canFinish"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["DFS", "BFS", "Graph", "Topological Sort"]
    parameters = ["numCourses: int", "prerequisites: List[List[int]]"]
    return_type = "bool"
    hidden_test_count = 4
    description = "Determine if you can finish all courses given prerequisites (cycle detection)."

    def get_test_cases(self):
        return [
            TestCase({"numCourses":2,"prerequisites":[[1,0]]}, True, "Example 1"),
            TestCase({"numCourses":2,"prerequisites":[[1,0],[0,1]]}, False, "Example 2: cycle"),
            TestCase({"numCourses":1,"prerequisites":[]}, True, "No prereqs"),
            TestCase({"numCourses":4,"prerequisites":[[1,0],[2,1],[3,2]]}, True, "Chain", is_hidden=True),
            TestCase({"numCourses":3,"prerequisites":[[0,1],[1,2],[2,0]]}, False, "Cycle of 3", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        n = inputs["numCourses"]
        adj = [[] for _ in range(n)]
        for a,b in inputs["prerequisites"]: adj[b].append(a)
        # 0=unvisited 1=visiting 2=done
        state = [0]*n
        def dfs(node):
            if state[node]==1: return False
            if state[node]==2: return True
            state[node]=1
            for nb in adj[node]:
                if not dfs(nb): return False
            state[node]=2
            return True
        return all(dfs(i) for i in range(n))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n=rng.randint(2,8)
            edges=[]
            for i in range(1,n):
                edges.append([i,rng.randint(0,i-1)])
            if rng.random()>0.5:
                # add a cycle
                edges.append([rng.randint(0,n-1),rng.randint(0,n-1)])
            tests.append({"numCourses":n,"prerequisites":edges})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 210 — Course Schedule II
# ═══════════════════════════════════════════════════════════════════════════
class CourseScheduleIIPlugin(ProblemPlugin):
    problem_id = "course-schedule-ii"
    leetcode_number = 210
    title = "Course Schedule II"
    slug = "course-schedule-ii"
    method_name = "findOrder"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["DFS", "BFS", "Graph", "Topological Sort"]
    parameters = ["numCourses: int", "prerequisites: List[List[int]]"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = "Return the ordering of courses to finish all. Return empty array if impossible."

    def get_test_cases(self):
        return [
            TestCase({"numCourses":2,"prerequisites":[[1,0]]}, [0,1], "Example 1"),
            TestCase({"numCourses":4,"prerequisites":[[1,0],[2,0],[3,1],[3,2]]}, [0,2,1,3], "Example 2"),
            TestCase({"numCourses":1,"prerequisites":[]}, [0], "Single course"),
            TestCase({"numCourses":2,"prerequisites":[[0,1],[1,0]]}, [], "Cycle", is_hidden=True),
        ]

    def get_validator(self): return TopSortValidator()

    @staticmethod
    def oracle(inputs):
        n = inputs["numCourses"]
        adj = [[] for _ in range(n)]
        indegree = [0]*n
        for a,b in inputs["prerequisites"]: adj[b].append(a); indegree[a]+=1
        from collections import deque
        q=deque(i for i in range(n) if indegree[i]==0)
        order=[]
        while q:
            node=q.popleft(); order.append(node)
            for nb in adj[node]:
                indegree[nb]-=1
                if indegree[nb]==0: q.append(nb)
        return order if len(order)==n else []

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n=rng.randint(2,6)
            edges=[[i,rng.randint(0,i-1)] for i in range(1,n)]
            tests.append({"numCourses":n,"prerequisites":edges})
        return tests

class TopSortValidator(Validator):
    """Validates topological ordering: correct length, all nodes present, prereqs satisfied."""
    def validate(self, actual, expected, inputs=None):
        if inputs is None: return EqualityValidator().validate(actual, expected)
        n = inputs.get("numCourses", 0)
        prereqs = inputs.get("prerequisites", [])
        # If expected is empty, both must be empty
        if not expected:
            passed = (actual == [])
            return ValidationResult(passed, repr(expected), repr(actual), "" if passed else "Expected empty")
        # Validate actual is a valid topological order
        if len(actual) != n or sorted(actual) != list(range(n)):
            return ValidationResult(False, repr(expected), repr(actual), "Not a valid permutation")
        pos = {v:i for i,v in enumerate(actual)}
        for a,b in prereqs:
            if pos[b] >= pos[a]:
                return ValidationResult(False, repr(expected), repr(actual), f"Prereq violated: {b} before {a}")
        return ValidationResult(True, repr(expected), repr(actual), "")


# ═══════════════════════════════════════════════════════════════════════════
# LC 323 — Number of Connected Components in an Undirected Graph
# ═══════════════════════════════════════════════════════════════════════════
class NumConnectedComponentsPlugin(ProblemPlugin):
    problem_id = "number-of-connected-components-in-an-undirected-graph"
    leetcode_number = 323
    title = "Number of Connected Components in an Undirected Graph"
    slug = "number-of-connected-components-in-an-undirected-graph"
    method_name = "countComponents"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["DFS", "BFS", "Union Find", "Graph"]
    parameters = ["n: int", "edges: List[List[int]]"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given n nodes and a list of undirected edges, return the number of connected components."

    def get_test_cases(self):
        return [
            TestCase({"n":5,"edges":[[0,1],[1,2],[3,4]]}, 2, "Example 1"),
            TestCase({"n":5,"edges":[[0,1],[1,2],[2,3],[3,4]]}, 1, "Example 2"),
            TestCase({"n":3,"edges":[]}, 3, "No edges"),
            TestCase({"n":1,"edges":[]}, 1, "Single node", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        n, edges = inputs["n"], inputs["edges"]
        adj = [[] for _ in range(n)]
        for u,v in edges: adj[u].append(v); adj[v].append(u)
        visited = [False]*n
        def dfs(node):
            visited[node]=True
            for nb in adj[node]:
                if not visited[nb]: dfs(nb)
        count=0
        for i in range(n):
            if not visited[i]: dfs(i); count+=1
        return count

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n=rng.randint(2,8)
            all_edges=[(i,j) for i in range(n) for j in range(i+1,n)]
            k=rng.randint(0,len(all_edges))
            edges=[list(e) for e in rng.sample(all_edges,k)]
            tests.append({"n":n,"edges":edges})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 684 — Redundant Connection
# ═══════════════════════════════════════════════════════════════════════════
class RedundantConnectionPlugin(ProblemPlugin):
    problem_id = "redundant-connection"
    leetcode_number = 684
    title = "Redundant Connection"
    slug = "redundant-connection"
    method_name = "findRedundantConnection"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["DFS", "BFS", "Union Find", "Graph"]
    parameters = ["edges: List[List[int]]"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = "Return the edge that can be removed to make the graph a tree."

    def get_test_cases(self):
        return [
            TestCase({"edges":[[1,2],[1,3],[2,3]]}, [2,3], "Example 1"),
            TestCase({"edges":[[1,2],[2,3],[3,4],[1,4],[1,5]]}, [1,4], "Example 2"),
            TestCase({"edges":[[1,2],[2,3],[1,3]]}, [1,3], "Triangle", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        edges = inputs["edges"]
        parent = list(range(max(max(e) for e in edges)+1))
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        def union(x,y):
            px,py=find(x),find(y)
            if px==py: return False
            parent[px]=py; return True
        for e in edges:
            if not union(e[0],e[1]): return e
        return []

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n=rng.randint(3,8)
            # Build a tree then add one edge
            edges=[[i, rng.randint(1,i)] for i in range(2,n+1)]
            # add redundant edge
            u,v=rng.sample(range(1,n+1),2)
            edges.append([min(u,v),max(u,v)])
            tests.append({"edges":edges})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 743 — Network Delay Time
# ═══════════════════════════════════════════════════════════════════════════
class NetworkDelayTimePlugin(ProblemPlugin):
    problem_id = "network-delay-time"
    leetcode_number = 743
    title = "Network Delay Time"
    slug = "network-delay-time"
    method_name = "networkDelayTime"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["DFS", "BFS", "Graph", "Heap (Priority Queue)", "Shortest Path"]
    parameters = ["times: List[List[int]]", "n: int", "k: int"]
    return_type = "int"
    hidden_test_count = 4
    description = "Find how long it takes for all n nodes to receive a signal from node k. Return -1 if impossible."

    def get_test_cases(self):
        return [
            TestCase({"times":[[2,1,1],[2,3,1],[3,4,1]],"n":4,"k":2}, 2, "Example 1"),
            TestCase({"times":[[1,2,1]],"n":2,"k":1}, 1, "Example 2"),
            TestCase({"times":[[1,2,1]],"n":2,"k":2}, -1, "Example 3: unreachable"),
            TestCase({"times":[[1,2,1],[2,3,2],[1,3,4]],"n":3,"k":1}, 3, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        import heapq
        times, n, k = inputs["times"], inputs["n"], inputs["k"]
        adj = [[] for _ in range(n+1)]
        for u,v,w in times: adj[u].append((v,w))
        dist = {k:0}
        heap = [(0,k)]
        while heap:
            d,u = heapq.heappop(heap)
            if d>dist.get(u,float('inf')): continue
            for v,w in adj[u]:
                nd=d+w
                if nd<dist.get(v,float('inf')):
                    dist[v]=nd; heapq.heappush(heap,(nd,v))
        if len(dist)<n: return -1
        return max(dist.values())

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n=rng.randint(2,6); k=rng.randint(1,n)
            nodes=list(range(1,n+1))
            edges=[]
            for u in nodes:
                for v in nodes:
                    if u!=v and rng.random()>0.5:
                        edges.append([u,v,rng.randint(1,10)])
            tests.append({"times":edges,"n":n,"k":k})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 787 — Cheapest Flights Within K Stops
# ═══════════════════════════════════════════════════════════════════════════
class CheapestFlightsPlugin(ProblemPlugin):
    problem_id = "cheapest-flights-within-k-stops"
    leetcode_number = 787
    title = "Cheapest Flights Within K Stops"
    slug = "cheapest-flights-within-k-stops"
    method_name = "findCheapestPrice"
    difficulty = "Medium"
    pattern = "Graphs"
    topics = ["Dynamic Programming", "DFS", "BFS", "Graph", "Heap", "Shortest Path"]
    parameters = ["n: int", "flights: List[List[int]]", "src: int", "dst: int", "k: int"]
    return_type = "int"
    hidden_test_count = 4
    description = "Find the cheapest price from src to dst with at most k stops. Return -1 if no route."

    def get_test_cases(self):
        return [
            TestCase({"n":4,"flights":[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],"src":0,"dst":3,"k":1}, 700, "Example 1"),
            TestCase({"n":3,"flights":[[0,1,100],[1,2,100],[0,2,500]],"src":0,"dst":2,"k":1}, 200, "Example 2"),
            TestCase({"n":3,"flights":[[0,1,100],[1,2,100],[0,2,500]],"src":0,"dst":2,"k":0}, 500, "k=0", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        n,flights,src,dst,k = inputs["n"],inputs["flights"],inputs["src"],inputs["dst"],inputs["k"]
        INF=float('inf')
        prices=[INF]*n; prices[src]=0
        for _ in range(k+1):
            tmp=prices[:]
            for u,v,w in flights:
                if prices[u]+w < tmp[v]: tmp[v]=prices[u]+w
            prices=tmp
        return prices[dst] if prices[dst]!=INF else -1

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n=rng.randint(3,6)
            flights=[[rng.randint(0,n-1),rng.randint(0,n-1),rng.randint(100,500)]
                     for _ in range(rng.randint(3,n*(n-1)))]
            flights=[[u,v,w] for u,v,w in flights if u!=v]
            src,dst=rng.sample(range(n),2)
            k=rng.randint(0,n-1)
            tests.append({"n":n,"flights":flights,"src":src,"dst":dst,"k":k})
        return tests
