# Overall Review

You have reached the end of ALG 1. You started with the question "What is an
algorithm?"; now you can tell in advance how code will behave as its input
grows, you know the hidden costs of Python's structures, you can search and
sort, and you can bring common problems down to `O(n)` with familiar
patterns. This section walks the path once more from start to end: at each
stop the most important idea and the code you will use most.

<figure class="fig">
  <div class="flow">
    <span class="node">Basics<br><small>00–02</small></span><span class="arrow">→</span>
    <span class="node">Search, sort<br><small>03–07</small></span><span class="arrow">→</span>
    <span class="node">Patterns<br><small>08–10</small></span><span class="arrow">→</span>
    <span class="node">Structures<br><small>11–12</small></span><span class="arrow">→</span>
    <span class="node acc">Trees<br><small>13–15</small></span>
  </div>
  <figcaption>The path of ALG 1: first measuring cost, then searching and sorting, then patterns and structures.</figcaption>
</figure>

## 1. Algorithms and complexity (Sections 0–1)

An algorithm: clear steps, in a set order, that turn input into output and
finish. Correctness is not working on an example but working **on every
input**: an empty list, a single element, negative numbers, all the same.

Algorithms are compared not in seconds but by **how the number of steps grows
as the input grows**. Big O keeps the dominant term:

| Class | Example | When n grows 1000 times |
|---|---|---|
| `O(1)` | dictionary lookup, `items[i]` on a list | the same |
| `O(log n)` | binary search | about 10 more steps |
| `O(n)` | `in` on a list, a single pass | 1000 times |
| `O(n log n)` | `sorted`, merge sort | a little over 1000 times |
| `O(n²)` | two nested loops | a million times |

Nested loops multiply, consecutive blocks add up, a loop that halves every
round is `O(log n)`.

## 2. The cost of Python's structures (Section 2)

| Operation | List | `deque` | Set / dictionary |
|---|---|---|---|
| `x in ...` | `O(n)` | `O(n)` | `O(1)` on average |
| Add at the end | `O(1)` amortised | `O(1)` | `O(1)` |
| Add at / take from the front | `O(n)` | `O(1)` | — |
| Access with `[i]` | `O(1)` | `O(n)` in the middle | — |

The most common mistake is the **one-line `O(n)`** inside a loop: `in`,
`index`, `count`, `remove`, `insert(0, …)`. Combined with the loop it
becomes `O(n²)`. In the lesson we measured a difference of thousands of
times between a list and a set over 1000 lookups.

## 3. Searching (Section 3)

Binary search on a sorted list drops half of the region every round,
`O(log n)`:

```python
def binary_search(items, target):
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

The ready-made one is `bisect`: `bisect_left` (the first fitting spot),
`bisect_right`, `insort`. Binary search works for any question whose answer
"changes after some point".

## 4. Sorting (Sections 4–7)

| Algorithm | Best | Average | Worst | Extra memory | Stable |
|---|---|---|---|---|---|
| Bubble, insertion | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | yes |
| Selection | `O(n²)` | `O(n²)` | `O(n²)` | `O(1)` | no |
| Merge sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)` | yes |
| Quick sort | `O(n log n)` | `O(n log n)` | `O(n²)` | avg. `O(log n)` | no |
| Heap sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(1)` | no |
| Counting (range `k`) | `O(n + k)` | `O(n + k)` | `O(n + k)` | `O(k)` | — |

Sorting by comparison cannot beat `n log n`; counting and radix sort go below
it because they do not compare. In real code use `sorted(items, key=...)`
(Timsort, stable); for several criteria a tuple key:
`key=lambda p: (-p[1], p[0])`.

## 5. Recursion and divide and conquer (Sections 5–6)

A recursive function calls itself with a **smaller** input; a **base case**
is required and every step must get closer to it. The calls pile up on the
call stack; in Python the depth limit is about 1000.

Divide and conquer: split, solve the pieces with yourself, combine. Merge
sort "splits in the middle and merges", quick sort "partitions around the
pivot". Recursion that solves the same subproblem over and over can grow
exponentially; the cure is dynamic programming in ALG 2.

## 6. Patterns that bring it down to O(n) (Sections 8–10)

| Question | Pattern | Cost |
|---|---|---|
| A pair with the target sum in a sorted list | two pointers, from both ends inwards | `O(n)` |
| The largest sum of `k` consecutive elements | fixed sliding window | `O(n)` |
| The longest stretch that meets a condition | variable window | `O(n)` |
| Many range sums | prefix sums: `prefix[hi] - prefix[lo]` | setup `O(n)`, each question `O(1)` |
| Seen before, how many times, is the complement there | set / dictionary | `O(n)` |

The common idea: if the pointers never move back, or each element enters a
dictionary once, the total work stays linear.

```python
seen = {}
for i, x in enumerate(nums):         # two-sum: look for the complement
    if target - x in seen:
        print(seen[target - x], i)
    seen[x] = i
```

## 7. Stacks, queues, linked lists (Sections 11–12)

- **Stack** (LIFO): a list with `append` / `pop`. Bracket checking, undo,
  postfix, the monotonic stack (the next greater element in `O(n)`).
- **Queue** (FIFO): a `deque` with `append` / `popleft`. Processing in order,
  BFS. `pop(0)` on a list is `O(n)`.
- **Linked list:** node = value + next. Adding at the front `O(1)`, the
  `i`-th element `O(n)`. Reversing with three pointers; cycle detection with
  the tortoise and the hare. LRU cache: dictionary + doubly linked list
  (`OrderedDict`).

## 8. Trees (Sections 13–15)

- **Tree:** the recursive skeleton: the base case if `None`, otherwise combine
  the two children's answers. DFS (preorder, inorder, postorder) with a
  stack, BFS with a queue.
- **BST:** the left subtree smaller, the right larger. Search, insert, delete
  `O(h)`; `O(log n)` if balanced, a chain if inserted sorted. Inorder gives
  sorted values.
- **Heap:** a gap-free tree + parent ≤ child, in a plain list. Adding and
  taking the smallest `O(log n)`; for the largest `k` a min-heap of size `k`,
  `O(n log k)`.

## Which tool for which question?

| Question | Think of first |
|---|---|
| "Is it in there?" many times | a set |
| "How many times does it appear?" | a dictionary counter |
| Search in sorted data, "the first/last fitting spot" | binary search, `bisect` |
| Consecutive stretches, subarrays | a sliding window or prefix sums |
| Matching brackets, "the last one opened" | a stack |
| Processing in order, fewest steps | a queue (BFS) |
| Always take the smallest/largest | a heap |
| Insert/delete keeping order, range queries | a BST or a sorted list + `bisect` |
| A nested structure | recursion |

## What comes next?

ALG 2 combines these tools: dynamic programming (solving recursion's repeated
subproblems once), greedy algorithms, backtracking (trying all possibilities
cleverly), graphs (BFS, Dijkstra, minimum spanning trees), string algorithms
and probabilistic data structures. In ALG 3 you will build data science and
machine learning algorithms from scratch with NumPy.
