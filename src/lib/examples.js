import { mockTrace, SAMPLE_CODE } from "./mockTrace";
import { binarySearchTrace, BINARY_SEARCH_CODE } from "./traces/binarySearch";
import { bubbleSortTrace, BUBBLE_SORT_CODE } from "./traces/bubbleSort";
import { fibonacciTrace, FIBONACCI_CODE } from "./traces/fibonacci";
import { stackTrace, STACK_CODE } from "./traces/stackTrace";
import { queueTrace, QUEUE_CODE } from "./traces/queueTrace";
import { linkedListTrace, LINKED_LIST_CODE } from "./traces/linkedListTrace";
import { treeTrace, TREE_CODE } from "./traces/treeTrace";
import { graphTrace, GRAPH_CODE } from "./traces/graphTrace";
import { heapTrace, HEAP_CODE } from "./traces/heapTrace";
import { dpGridTrace, DP_GRID_CODE } from "./traces/dpGridTrace";

export const EXAMPLES = [
  { key: "topk", label: "Top K Frequent", code: SAMPLE_CODE, trace: mockTrace },
  { key: "binary_search", label: "Binary Search", code: BINARY_SEARCH_CODE, trace: binarySearchTrace },
  { key: "bubble_sort", label: "Bubble Sort", code: BUBBLE_SORT_CODE, trace: bubbleSortTrace },
  { key: "fibonacci", label: "Fibonacci (Memoized)", code: FIBONACCI_CODE, trace: fibonacciTrace },
  { key: "stack", label: "Stack (Push/Pop)", code: STACK_CODE, trace: stackTrace },
  { key: "queue", label: "Queue (Enqueue/Dequeue)", code: QUEUE_CODE, trace: queueTrace },
  { key: "linked_list", label: "Linked List", code: LINKED_LIST_CODE, trace: linkedListTrace },
  { key: "tree", label: "BST Insert", code: TREE_CODE, trace: treeTrace },
  { key: "graph", label: "Graph BFS", code: GRAPH_CODE, trace: graphTrace },
  { key: "heap", label: "Heap Heapify", code: HEAP_CODE, trace: heapTrace },
  { key: "dp_grid", label: "DP Grid (Unique Paths)", code: DP_GRID_CODE, trace: dpGridTrace },
];