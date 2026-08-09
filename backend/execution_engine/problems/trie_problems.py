"""Trie pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase, WrapperTemplate
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult
from backend.execution_engine.object_builder import TRIE_NODE_HELPERS


# ═══════════════════════════════════════════════════════════════════════════
# LC 208 — Implement Trie (Prefix Tree)  (stateful)
# ═══════════════════════════════════════════════════════════════════════════
_TRIE_TPL = """{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = Trie()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "insert":
            obj.insert(arg[0]); out.append(None)
        elif op == "search":
            out.append(obj.search(arg[0]))
        elif op == "startsWith":
            out.append(obj.startsWith(arg[0]))
        else:
            out.append(None)
    print("__RESULT__:")
    print(repr(out))

main()
"""

class TriePlugin(ProblemPlugin):
    problem_id = "implement-trie-prefix-tree"
    leetcode_number = 208
    title = "Implement Trie (Prefix Tree)"
    slug = "implement-trie-prefix-tree"
    method_name = "insert"
    difficulty = "Medium"
    pattern = "Tries"
    topics = ["Hash Table", "String", "Design", "Trie"]
    parameters = ["word: str"]
    return_type = "None"
    hidden_test_count = 3
    stateful = True
    description = "Implement a trie with insert, search, and startsWith methods."

    def get_test_cases(self):
        return [
            TestCase(
                {"ops":["Trie","insert","search","search","startsWith","insert","search"],
                 "args":[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]},
                [None,None,True,False,True,None,True], "Example 1"
            ),
            TestCase(
                {"ops":["Trie","insert","search","startsWith"],
                 "args":[[],["hello"],["hello"],["hel"]]},
                [None,None,True,True], "Simple", is_hidden=True
            ),
        ]

    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_TRIE_TPL)

    @staticmethod
    def oracle(inputs):
        ops, args = inputs["ops"], inputs["args"]
        words = set()
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "insert": words.add(arg[0]); out.append(None)
            elif op == "search": out.append(arg[0] in words)
            elif op == "startsWith": out.append(any(w.startswith(arg[0]) for w in words))
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for _ in range(count):
            vocab = ["".join(rng.choices(string.ascii_lowercase[:8], k=rng.randint(1,5))) for _ in range(5)]
            ops=["Trie"]; args=[[]]
            for w in vocab: ops.append("insert"); args.append([w])
            for _ in range(rng.randint(3,6)):
                op=rng.choice(["search","startsWith"])
                w=rng.choice(vocab) if rng.random()>0.4 else rng.choice(string.ascii_lowercase[:8])
                ops.append(op); args.append([w])
            tests.append({"ops":ops,"args":args})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 211 — Design Add and Search Words Data Structure  (stateful)
# ═══════════════════════════════════════════════════════════════════════════
_WORD_DICT_TPL = """{imports}
{helpers}
{solution_code}

def main():
    ops  = {ops}
    args = {args}
    out  = [None]
    obj  = WordDictionary()
    for op, arg in zip(ops[1:], args[1:]):
        if op == "addWord":
            obj.addWord(arg[0]); out.append(None)
        elif op == "search":
            out.append(obj.search(arg[0]))
        else:
            out.append(None)
    print("__RESULT__:")
    print(repr(out))

main()
"""

class WordDictionaryPlugin(ProblemPlugin):
    problem_id = "design-add-and-search-words-data-structure"
    leetcode_number = 211
    title = "Design Add and Search Words Data Structure"
    slug = "design-add-and-search-words-data-structure"
    method_name = "addWord"
    difficulty = "Medium"
    pattern = "Tries"
    topics = ["String", "DFS", "Design", "Trie"]
    parameters = ["word: str"]
    return_type = "None"
    hidden_test_count = 3
    stateful = True
    description = "Design a data structure that supports addWord and search (with '.' wildcard)."

    def get_test_cases(self):
        return [
            TestCase(
                {"ops":["WordDictionary","addWord","addWord","addWord","search","search","search","search"],
                 "args":[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]},
                [None,None,None,None,False,True,True,True], "Example 1"
            ),
            TestCase(
                {"ops":["WordDictionary","addWord","search"],
                 "args":[[],["abc"],["a.c"]]},
                [None,None,True], "Wildcard", is_hidden=True
            ),
        ]

    def get_validator(self): return EqualityValidator()
    def get_wrapper_template(self): return WrapperTemplate(template_str=_WORD_DICT_TPL)

    @staticmethod
    def oracle(inputs):
        import re
        ops, args = inputs["ops"], inputs["args"]
        words = []
        out = [None]
        for op, arg in zip(ops[1:], args[1:]):
            if op == "addWord": words.append(arg[0]); out.append(None)
            elif op == "search":
                pat = arg[0].replace(".", "[a-z]")
                out.append(any(re.fullmatch(pat, w) for w in words))
        return out

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for _ in range(count):
            vocab=["".join(rng.choices(string.ascii_lowercase[:6],k=3)) for _ in range(5)]
            ops=["WordDictionary"]; args=[[]]
            for w in vocab: ops.append("addWord"); args.append([w])
            for _ in range(4):
                w=list(rng.choice(vocab))
                for i in rng.sample(range(len(w)),rng.randint(0,1)): w[i]="."
                ops.append("search"); args.append(["".join(w)])
            tests.append({"ops":ops,"args":args})
        return tests


# ═══════════════════════════════════════════════════════════════════════════
# LC 212 — Word Search II
# ═══════════════════════════════════════════════════════════════════════════
class WordSearchIIPlugin(ProblemPlugin):
    problem_id = "word-search-ii"
    leetcode_number = 212
    title = "Word Search II"
    slug = "word-search-ii"
    method_name = "findWords"
    difficulty = "Hard"
    pattern = "Tries"
    topics = ["Array", "String", "Backtracking", "Trie", "Matrix"]
    parameters = ["board: List[List[str]]", "words: List[str]"]
    return_type = "List[str]"
    hidden_test_count = 3
    description = "Given a board and a list of words, find all words that exist in the board."

    def get_test_cases(self):
        return [
            TestCase({"board":[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
                      "words":["oath","pea","eat","rain"]}, ["eat","oath"], "Example 1"),
            TestCase({"board":[["a","b"],["c","d"]],"words":["abcb"]}, [], "Example 2: not found"),
        ]

    def get_validator(self):
        from backend.execution_engine.problems._validators import SetValidator
        return SetValidator()

    @staticmethod
    def oracle(inputs):
        board, words = inputs["board"], inputs["words"]
        rows, cols = len(board), len(board[0]) if board else 0
        found = set()
        word_set = set(words)
        def dfs(r, c, node, path, visited):
            if path in word_set: found.add(path)
            if r<0 or r>=rows or c<0 or c>=cols or (r,c) in visited: return
            visited.add((r,c))
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                dfs(r+dr,c+dc,node,path+board[r+dr][c+dc] if 0<=r+dr<rows and 0<=c+dc<cols else path, visited)
            visited.remove((r,c))
        # Simple: check each word by DFS
        def exists(word):
            def dfs2(r,c,i,visited):
                if i==len(word): return True
                if r<0 or r>=rows or c<0 or c>=cols or (r,c) in visited or board[r][c]!=word[i]: return False
                visited.add((r,c))
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    if dfs2(r+dr,c+dc,i+1,visited): visited.remove((r,c)); return True
                visited.remove((r,c)); return False
            for r in range(rows):
                for c in range(cols):
                    if dfs2(r,c,0,set()): return True
            return False
        return sorted(w for w in words if exists(w))

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            letters="abcdef"
            board=[[rng.choice(letters) for _ in range(4)] for _ in range(4)]
            flat="".join(c for row in board for c in row)
            words=[]
            for _ in range(5):
                l=rng.randint(2,4)
                words.append("".join(rng.choices(letters,k=l)))
            tests.append({"board":board,"words":list(set(words))})
        return tests
