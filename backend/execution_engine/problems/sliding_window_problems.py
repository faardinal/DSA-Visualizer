"""Sliding Window pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator


# ---------------------------------------------------------------------------
# Best Time to Buy and Sell Stock  (LC 121)
# ---------------------------------------------------------------------------
class BestTimeBuySellStockPlugin(ProblemPlugin):
    problem_id = "best-time-to-buy-and-sell-stock"
    leetcode_number = 121
    slug = "best-time-to-buy-and-sell-stock"
    title = "Best Time to Buy and Sell Stock"
    method_name = "maxProfit"
    difficulty = "Easy"
    pattern = "Sliding Window"
    topics = ["Array", "Dynamic Programming"]
    parameters = ["prices: List[int]"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "You are given an array prices where prices[i] is the price of a given stock on the ith day. "
        "Return the maximum profit you can achieve."
    )

    def get_test_cases(self):
        return [
            TestCase({"prices": [7,1,5,3,6,4]}, 5, "Example 1"),
            TestCase({"prices": [7,6,4,3,1]}, 0, "Example 2: no profit"),
            TestCase({"prices": [1,2]}, 1, "Two days", is_hidden=True),
            TestCase({"prices": [2,1,4]}, 3, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        prices = inputs["prices"]
        best, min_price = 0, float('inf')
        for p in prices:
            min_price = min(min_price, p)
            best = max(best, p - min_price)
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(2, 20)
            tests.append({"prices": [rng.randint(1, 100) for _ in range(n)]})
        return tests


# ---------------------------------------------------------------------------
# Longest Substring Without Repeating Characters  (LC 3)
# ---------------------------------------------------------------------------
class LongestSubstringNoRepeatPlugin(ProblemPlugin):
    problem_id = "longest-substring-without-repeating-characters"
    leetcode_number = 3
    slug = "longest-substring-without-repeating-characters"
    title = "Longest Substring Without Repeating Characters"
    method_name = "lengthOfLongestSubstring"
    difficulty = "Medium"
    pattern = "Sliding Window"
    topics = ["Hash Table", "String", "Sliding Window"]
    parameters = ["s: str"]
    return_type = "int"
    hidden_test_count = 4
    description = "Given a string s, find the length of the longest substring without repeating characters."

    def get_test_cases(self):
        return [
            TestCase({"s": "abcabcbb"}, 3, "Example 1"),
            TestCase({"s": "bbbbb"}, 1, "Example 2"),
            TestCase({"s": "pwwkew"}, 3, "Example 3"),
            TestCase({"s": ""}, 0, "Empty string", is_hidden=True),
            TestCase({"s": "au"}, 2, "Two chars", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s = inputs["s"]
        seen = {}
        l = best = 0
        for r, c in enumerate(s):
            if c in seen and seen[c] >= l:
                l = seen[c] + 1
            seen[c] = r
            best = max(best, r - l + 1)
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for _ in range(count):
            chars = string.ascii_lowercase[:10]
            s = "".join(rng.choices(chars, k=rng.randint(0, 20)))
            tests.append({"s": s})
        return tests


# ---------------------------------------------------------------------------
# Longest Repeating Character Replacement  (LC 424)
# ---------------------------------------------------------------------------
class LongestRepeatingCharReplacementPlugin(ProblemPlugin):
    problem_id = "longest-repeating-character-replacement"
    leetcode_number = 424
    slug = "longest-repeating-character-replacement"
    title = "Longest Repeating Character Replacement"
    method_name = "characterReplacement"
    difficulty = "Medium"
    pattern = "Sliding Window"
    topics = ["Hash Table", "String", "Sliding Window"]
    parameters = ["s: str", "k: int"]
    return_type = "int"
    hidden_test_count = 4
    description = (
        "You are given a string s and an integer k. You can choose any character of the string and "
        "change it to any other uppercase English character. You can perform this operation at most k times. "
        "Return the length of the longest substring containing the same letter you can get after performing the above operations."
    )

    def get_test_cases(self):
        return [
            TestCase({"s": "ABAB", "k": 2}, 4, "Example 1"),
            TestCase({"s": "AABABBA", "k": 1}, 4, "Example 2"),
            TestCase({"s": "A", "k": 0}, 1, "Single char", is_hidden=True),
            TestCase({"s": "AAAA", "k": 2}, 4, "All same", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s, k = inputs["s"], inputs["k"]
        count = {}
        l = best = max_count = 0
        for r, c in enumerate(s):
            count[c] = count.get(c, 0) + 1
            max_count = max(max_count, count[c])
            while (r - l + 1) - max_count > k:
                count[s[l]] -= 1
                l += 1
            best = max(best, r - l + 1)
        return best

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(1, 20)
            s = "".join(rng.choices("ABCDE", k=n))
            k = rng.randint(0, n // 2)
            tests.append({"s": s, "k": k})
        return tests


# ---------------------------------------------------------------------------
# Permutation in String  (LC 567)
# ---------------------------------------------------------------------------
class PermutationInStringPlugin(ProblemPlugin):
    problem_id = "permutation-in-string"
    leetcode_number = 567
    slug = "permutation-in-string"
    title = "Permutation in String"
    method_name = "checkInclusion"
    difficulty = "Medium"
    pattern = "Sliding Window"
    topics = ["Hash Table", "Two Pointers", "String", "Sliding Window"]
    parameters = ["s1: str", "s2: str"]
    return_type = "bool"
    hidden_test_count = 4
    description = (
        "Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise."
    )

    def get_test_cases(self):
        return [
            TestCase({"s1": "ab", "s2": "eidbaooo"}, True, "Example 1"),
            TestCase({"s1": "ab", "s2": "eidboaoo"}, False, "Example 2"),
            TestCase({"s1": "a", "s2": "a"}, True, "Single char", is_hidden=True),
            TestCase({"s1": "abc", "s2": "bbbca"}, True, "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import Counter
        s1, s2 = inputs["s1"], inputs["s2"]
        if len(s1) > len(s2): return False
        need = Counter(s1)
        window = Counter(s2[:len(s1)])
        if window == need: return True
        for i in range(len(s1), len(s2)):
            c_in = s2[i]
            c_out = s2[i - len(s1)]
            window[c_in] += 1
            window[c_out] -= 1
            if window[c_out] == 0: del window[c_out]
            if window == need: return True
        return False

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for i in range(count):
            chars = string.ascii_lowercase[:6]
            s1 = "".join(rng.choices(chars, k=rng.randint(1, 5)))
            base = "".join(rng.choices(chars, k=rng.randint(5, 15)))
            if i % 2 == 0:
                import random
                pos = rng.randint(0, len(base))
                perm = list(s1); rng.shuffle(perm)
                s2 = base[:pos] + "".join(perm) + base[pos:]
            else:
                s2 = base
            tests.append({"s1": s1, "s2": s2})
        return tests


# ---------------------------------------------------------------------------
# Minimum Window Substring  (LC 76)
# ---------------------------------------------------------------------------
class MinWindowSubstringPlugin(ProblemPlugin):
    problem_id = "minimum-window-substring"
    leetcode_number = 76
    slug = "minimum-window-substring"
    title = "Minimum Window Substring"
    method_name = "minWindow"
    difficulty = "Hard"
    pattern = "Sliding Window"
    topics = ["Hash Table", "String", "Sliding Window"]
    parameters = ["s: str", "t: str"]
    return_type = "str"
    hidden_test_count = 4
    description = (
        "Given two strings s and t of lengths m and n, return the minimum window substring of s "
        "such that every character in t (including duplicates) is included in the window."
    )

    def get_test_cases(self):
        return [
            TestCase({"s": "ADOBECODEBANC", "t": "ABC"}, "BANC", "Example 1"),
            TestCase({"s": "a", "t": "a"}, "a", "Example 2"),
            TestCase({"s": "a", "t": "aa"}, "", "Example 3: impossible"),
            TestCase({"s": "abc", "t": "b"}, "b", "Hidden", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import Counter
        s, t = inputs["s"], inputs["t"]
        if not t or not s: return ""
        need = Counter(t)
        have, total = 0, len(need)
        window = {}
        l = 0
        best = (float('inf'), 0, 0)
        for r, c in enumerate(s):
            window[c] = window.get(c, 0) + 1
            if c in need and window[c] == need[c]: have += 1
            while have == total:
                if (r - l + 1) < best[0]:
                    best = (r - l + 1, l, r)
                lc = s[l]
                window[lc] -= 1
                if lc in need and window[lc] < need[lc]: have -= 1
                l += 1
        return s[best[1]:best[2]+1] if best[0] != float('inf') else ""

    @staticmethod
    def generate_hidden_inputs(rng, count):
        import string
        tests = []
        for i in range(count):
            chars = string.ascii_uppercase[:8]
            t = "".join(rng.choices(chars, k=rng.randint(1, 4)))
            if i % 2 == 0:
                extra = "".join(rng.choices(chars, k=rng.randint(3, 8)))
                pos = rng.randint(0, len(extra))
                s = extra[:pos] + t + extra[pos:]
            else:
                s = "".join(rng.choices(chars, k=rng.randint(4, 15)))
            tests.append({"s": s, "t": t})
        return tests


# ---------------------------------------------------------------------------
# Sliding Window Maximum  (LC 239)
# ---------------------------------------------------------------------------
class SlidingWindowMaximumPlugin(ProblemPlugin):
    problem_id = "sliding-window-maximum"
    leetcode_number = 239
    slug = "sliding-window-maximum"
    title = "Sliding Window Maximum"
    method_name = "maxSlidingWindow"
    difficulty = "Hard"
    pattern = "Sliding Window"
    topics = ["Array", "Queue", "Sliding Window", "Heap", "Monotonic Queue"]
    parameters = ["nums: List[int]", "k: int"]
    return_type = "List[int]"
    hidden_test_count = 4
    description = (
        "You are given an array of integers nums, there is a sliding window of size k which is moving "
        "from the very left of the array to the very right. Return the max sliding window."
    )

    def get_test_cases(self):
        return [
            TestCase({"nums": [1,3,-1,-3,5,3,6,7], "k": 3}, [3,3,5,5,6,7], "Example 1"),
            TestCase({"nums": [1], "k": 1}, [1], "Example 2"),
            TestCase({"nums": [1,-1], "k": 1}, [1,-1], "k=1", is_hidden=True),
        ]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import deque
        nums, k = inputs["nums"], inputs["k"]
        dq = deque()
        result = []
        for i, n in enumerate(nums):
            while dq and nums[dq[-1]] <= n: dq.pop()
            dq.append(i)
            if dq[0] == i - k: dq.popleft()
            if i >= k - 1: result.append(nums[dq[0]])
        return result

    @staticmethod
    def generate_hidden_inputs(rng, count):
        tests = []
        for _ in range(count):
            n = rng.randint(3, 20)
            nums = [rng.randint(-10, 10) for _ in range(n)]
            k = rng.randint(1, n)
            tests.append({"nums": nums, "k": k})
        return tests
