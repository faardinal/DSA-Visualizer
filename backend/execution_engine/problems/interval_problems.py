"""Intervals pattern problems."""
from backend.execution_engine.plugin_base import ProblemPlugin, TestCase
from backend.execution_engine.problems._validators import EqualityValidator


# LC 57 — Insert Interval
class InsertIntervalPlugin(ProblemPlugin):
    problem_id="insert-interval"; leetcode_number=57; title="Insert Interval"; slug="insert-interval"
    method_name="insert"; difficulty="Medium"; pattern="Intervals"
    topics=["Array"]; parameters=["intervals: List[List[int]]","newInterval: List[int]"]
    return_type="List[List[int]]"; hidden_test_count=4
    description="Insert newInterval into a list of non-overlapping sorted intervals and merge if needed."

    def get_test_cases(self):
        return [TestCase({"intervals":[[1,3],[6,9]],"newInterval":[2,5]},[[1,5],[6,9]],"Example 1"),
                TestCase({"intervals":[[1,2],[3,5],[6,7],[8,10],[12,16]],"newInterval":[4,8]},
                         [[1,2],[3,10],[12,16]],"Example 2"),
                TestCase({"intervals":[],"newInterval":[5,7]},[[5,7]],"Empty intervals",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        intervals,ni=inputs["intervals"],inputs["newInterval"]
        result=[]; i=0; n=len(intervals)
        while i<n and intervals[i][1]<ni[0]: result.append(intervals[i]); i+=1
        while i<n and intervals[i][0]<=ni[1]: ni=[min(ni[0],intervals[i][0]),max(ni[1],intervals[i][1])]; i+=1
        result.append(ni)
        while i<n: result.append(intervals[i]); i+=1
        return result

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            starts=sorted(rng.sample(range(1,30),rng.randint(2,8)))
            intervals=[[s,s+rng.randint(1,4)] for s in starts]
            # merge overlaps
            merged=[]
            for iv in intervals:
                if merged and iv[0]<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],iv[1])
                else: merged.append(iv[:])
            ni=[rng.randint(1,20),rng.randint(1,30)]; ni.sort()
            tests.append({"intervals":merged,"newInterval":ni})
        return tests


# LC 56 — Merge Intervals
class MergeIntervalsPlugin(ProblemPlugin):
    problem_id="merge-intervals"; leetcode_number=56; title="Merge Intervals"; slug="merge-intervals"
    method_name="merge"; difficulty="Medium"; pattern="Intervals"
    topics=["Array","Sorting"]; parameters=["intervals: List[List[int]]"]
    return_type="List[List[int]]"; hidden_test_count=4; description="Merge all overlapping intervals."

    def get_test_cases(self):
        return [TestCase({"intervals":[[1,3],[2,6],[8,10],[15,18]]},[[1,6],[8,10],[15,18]],"Example 1"),
                TestCase({"intervals":[[1,4],[4,5]]},[[1,5]],"Example 2"),
                TestCase({"intervals":[[1,4]]},[[1,4]],"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        ivs=sorted(inputs["intervals"]); merged=[]
        for iv in ivs:
            if merged and iv[0]<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],iv[1])
            else: merged.append(iv[:])
        return merged

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,10)
            tests.append({"intervals":[[rng.randint(0,20),rng.randint(1,25)] for _ in range(n)]})
        return tests


# LC 435 — Non-overlapping Intervals
class NonOverlappingIntervalsPlugin(ProblemPlugin):
    problem_id="non-overlapping-intervals"; leetcode_number=435; title="Non-overlapping Intervals"
    slug="non-overlapping-intervals"; method_name="eraseOverlapIntervals"; difficulty="Medium"
    pattern="Intervals"; topics=["Array","Dynamic Programming","Greedy","Sorting"]
    parameters=["intervals: List[List[int]]"]; return_type="int"; hidden_test_count=4
    description="Return minimum number of intervals to remove to make the rest non-overlapping."

    def get_test_cases(self):
        return [TestCase({"intervals":[[1,2],[2,3],[3,4],[1,3]]},1,"Example 1"),
                TestCase({"intervals":[[1,2],[1,2],[1,2]]},2,"Example 2"),
                TestCase({"intervals":[[1,2],[2,3]]},0,"No overlap",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        ivs=sorted(inputs["intervals"],key=lambda x:x[1]); remove=0; end=float('-inf')
        for s,e in ivs:
            if s>=end: end=e
            else: remove+=1
        return remove

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,10)
            tests.append({"intervals":[[rng.randint(0,10),rng.randint(1,12)] for _ in range(n)]})
        return tests


# LC 252 — Meeting Rooms
class MeetingRoomsPlugin(ProblemPlugin):
    problem_id="meeting-rooms"; leetcode_number=252; title="Meeting Rooms"; slug="meeting-rooms"
    method_name="canAttendMeetings"; difficulty="Easy"; pattern="Intervals"
    topics=["Array","Sorting"]; parameters=["intervals: List[List[int]]"]
    return_type="bool"; hidden_test_count=4; description="Return true if a person can attend all meetings."

    def get_test_cases(self):
        return [TestCase({"intervals":[[0,30],[5,10],[15,20]]},False,"Example 1"),
                TestCase({"intervals":[[7,10],[2,4]]},True,"Example 2"),
                TestCase({"intervals":[]},True,"Empty",is_hidden=True),
                TestCase({"intervals":[[1,2]]},True,"Single",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        ivs=sorted(inputs["intervals"])
        for i in range(1,len(ivs)):
            if ivs[i][0]<ivs[i-1][1]: return False
        return True

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for i in range(count):
            n=rng.randint(2,8)
            if i%2==0:
                starts=sorted(rng.sample(range(0,100,10),n))
                ivs=[[s,s+5] for s in starts]
            else:
                ivs=[[rng.randint(0,20),rng.randint(1,25)] for _ in range(n)]
            tests.append({"intervals":ivs})
        return tests


# LC 253 — Meeting Rooms II
class MeetingRoomsIIPlugin(ProblemPlugin):
    problem_id="meeting-rooms-ii"; leetcode_number=253; title="Meeting Rooms II"; slug="meeting-rooms-ii"
    method_name="minMeetingRooms"; difficulty="Medium"; pattern="Intervals"
    topics=["Array","Two Pointers","Greedy","Sorting","Heap"]; parameters=["intervals: List[List[int]]"]
    return_type="int"; hidden_test_count=4; description="Return minimum number of conference rooms required."

    def get_test_cases(self):
        return [TestCase({"intervals":[[0,30],[5,10],[15,20]]},2,"Example 1"),
                TestCase({"intervals":[[7,10],[2,4]]},1,"Example 2"),
                TestCase({"intervals":[[1,5],[2,6],[3,7]]},3,"All overlap",is_hidden=True)]

    def get_validator(self): return EqualityValidator()

    @staticmethod
    def oracle(inputs):
        import heapq
        ivs=sorted(inputs["intervals"]); heap=[]
        for s,e in ivs:
            if heap and heap[0]<=s: heapq.heapreplace(heap,e)
            else: heapq.heappush(heap,e)
        return len(heap)

    @staticmethod
    def generate_hidden_inputs(rng,count):
        tests=[]
        for _ in range(count):
            n=rng.randint(2,10)
            tests.append({"intervals":[[rng.randint(0,20),rng.randint(1,25)] for _ in range(n)]})
        return tests
