"""Greedy pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator, Validator, ValidationResult


# LC 53 — Maximum Subarray
class MaxSubarrayPlugin(ProblemPlugin):
    problem_id="maximum-subarray"; leetcode_number=53; title="Maximum Subarray"; slug="maximum-subarray"
    method_name="maxSubArray"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Divide and Conquer","Dynamic Programming"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4; description="Find the subarray with the largest sum and return its sum."

    def get_test_cases(self):
        return [TestCase({"nums":[-2,1,-3,4,-1,2,1,-5,4]},6,"Example 1"),
                TestCase({"nums":[1]},1,"Single"),TestCase({"nums":[5,4,-1,7,8]},23,"Example 3"),
                TestCase({"nums":[-1,-2,-3]},-1,"All neg",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; best=cur=nums[0]
        for n in nums[1:]: cur=max(n,cur+n); best=max(best,cur)
        return best

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(-10,10) for _ in range(rng.randint(1,20))]} for _ in range(count)]


# LC 55 — Jump Game
class JumpGamePlugin(ProblemPlugin):
    problem_id="jump-game"; leetcode_number=55; title="Jump Game"; slug="jump-game"
    method_name="canJump"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Dynamic Programming","Greedy"]; parameters=["nums: List[int]"]
    return_type="bool"; hidden_test_count=4; description="Return true if you can reach the last index."

    def get_test_cases(self):
        return [TestCase({"nums":[2,3,1,1,4]},True,"Example 1"),
                TestCase({"nums":[3,2,1,0,4]},False,"Example 2"),
                TestCase({"nums":[0]},True,"Single zero"),
                TestCase({"nums":[1,0,0]},False,"Can't pass",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; reach=0
        for i,n in enumerate(nums):
            if i>reach: return False
            reach=max(reach,i+n)
        return True

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            n=rng.randint(2,15)
            if i%2==0: nums=[rng.randint(1,n) for _ in range(n)]
            else: nums=[rng.randint(0,2) for _ in range(n)]
            tests.append({"nums":nums})
        return tests


# LC 45 — Jump Game II
class JumpGameIIPlugin(ProblemPlugin):
    problem_id="jump-game-ii"; leetcode_number=45; title="Jump Game II"; slug="jump-game-ii"
    method_name="jump"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Dynamic Programming","Greedy"]; parameters=["nums: List[int]"]
    return_type="int"; hidden_test_count=4; description="Return minimum jumps to reach last index."

    def get_test_cases(self):
        return [TestCase({"nums":[2,3,1,1,4]},2,"Example 1"),TestCase({"nums":[2,3,0,1,4]},2,"Example 2"),
                TestCase({"nums":[0]},0,"Single",is_hidden=True),TestCase({"nums":[1,2,3]},2,"Chain",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        nums=inputs["nums"]; jumps=cur_end=far=0
        for i in range(len(nums)-1):
            far=max(far,i+nums[i])
            if i==cur_end: jumps+=1; cur_end=far
        return jumps

    @staticmethod
    def generate_hidden_inputs(rng,count):
        return [{"nums":[rng.randint(1,5) for _ in range(rng.randint(2,15))]} for _ in range(count)]


# LC 134 — Gas Station
class GasStationPlugin(ProblemPlugin):
    problem_id="gas-station"; leetcode_number=134; title="Gas Station"; slug="gas-station"
    method_name="canCompleteCircuit"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Greedy"]; parameters=["gas: List[int]","cost: List[int]"]
    return_type="int"; hidden_test_count=4; description="Return the starting station index for a circular route, or -1."

    def get_test_cases(self):
        return [TestCase({"gas":[1,2,3,4,5],"cost":[3,4,5,1,2]},3,"Example 1"),
                TestCase({"gas":[2,3,4],"cost":[3,4,3]},-1,"Example 2"),
                TestCase({"gas":[5],"cost":[4]},0,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        gas,cost=inputs["gas"],inputs["cost"]
        if sum(gas)<sum(cost): return -1
        tank=start=0
        for i in range(len(gas)):
            tank+=gas[i]-cost[i]
            if tank<0: tank=0; start=i+1
        return start

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            n=rng.randint(2,10)
            gas=[rng.randint(1,10) for _ in range(n)]
            cost=[rng.randint(1,10) for _ in range(n)]
            if i%2==0: cost=[min(g,c) for g,c in zip(gas,cost)]  # ensure solution exists
            tests.append({"gas":gas,"cost":cost})
        return tests


# LC 846 — Hand of Straights
class HandOfStraightsPlugin(ProblemPlugin):
    problem_id="hand-of-straights"; leetcode_number=846; title="Hand of Straights"; slug="hand-of-straights"
    method_name="isNStraightHand"; difficulty="Medium"; pattern="Greedy"
    topics=["Array","Hash Table","Greedy","Sorting"]; parameters=["hand: List[int]","groupSize: int"]
    return_type="bool"; hidden_test_count=4; description="Return true if hand can be rearranged into groups of groupSize consecutive cards."

    def get_test_cases(self):
        return [TestCase({"hand":[1,2,3,6,2,3,4,7,8],"groupSize":3},True,"Example 1"),
                TestCase({"hand":[1,2,3,4,5],"groupSize":4},False,"Example 2"),
                TestCase({"hand":[1],"groupSize":1},True,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        from collections import Counter
        hand,gs=inputs["hand"],inputs["groupSize"]
        if len(hand)%gs!=0: return False
        cnt=Counter(hand)
        for k in sorted(cnt):
            if cnt[k]>0:
                n=cnt[k]
                for i in range(gs):
                    if cnt[k+i]<n: return False
                    cnt[k+i]-=n
        return True

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            gs=rng.randint(2,4); groups=rng.randint(1,5)
            hand=[]
            for _ in range(groups):
                start=rng.randint(1,10)
                hand.extend(range(start,start+gs))
            rng.shuffle(hand)
            tests.append({"hand":hand,"groupSize":gs})
        return tests


# LC 763 — Partition Labels
class PartitionLabelsPlugin(ProblemPlugin):
    problem_id="partition-labels"; leetcode_number=763; title="Partition Labels"; slug="partition-labels"
    method_name="partitionLabels"; difficulty="Medium"; pattern="Greedy"
    topics=["Hash Table","Two Pointers","String","Greedy"]; parameters=["s: str"]
    return_type="List[int]"; hidden_test_count=4; description="Return a list of integers representing partition sizes."

    def get_test_cases(self):
        return [TestCase({"s":"ababcbacadefegdehijhklij"},[9,7,8],"Example 1"),
                TestCase({"s":"eccbbbbdec"},[10],"Example 2"),
                TestCase({"s":"a"},[1],"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        s=inputs["s"]; last={c:i for i,c in enumerate(s)}
        result=[]; start=end=0
        for i,c in enumerate(s):
            end=max(end,last[c])
            if i==end: result.append(end-start+1); start=i+1
        return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        import string
        return [{"s":"".join(rng.choices(string.ascii_lowercase[:6],k=rng.randint(3,20)))} for _ in range(count)]
