# Problem-Solving Patterns

When you meet a new problem, you usually do not invent an algorithm from
scratch; you recognise which **pattern** the problem resembles. This section
does two things: first it estimates which complexity is enough from the size of
the input, then it shows four patterns we have not seen yet, by measuring.

## Budget first: what does the input size say?

In a loop, Python takes roughly ten million simple steps a second (it varies a
few times by machine). The size of the input largely decides which complexity
will fit:

| `n` at most | Complexity that fits | Pattern that comes to mind |
|---|---|---|
| ~20 | `O(2ⁿ)` | all subsets, backtracking |
| ~40 | `O(2^(n/2))` | meet in the middle |
| ~1,000 | `O(n²)` | nested loops, a DP table |
| ~1,000,000 | `O(n log n)`, `O(n)` | sorting, two pointers, hashing, a stack |
| very large | `O(log n)`, `O(1)` | binary search, a formula |

This table is not a strict rule but a starting point: if you see
`n = 100,000`, you rule out nested loops from the start.

## Binary search on the answer

In some problems asking "at least how many?" or "at most how many?", finding
the answer directly is hard, but checking whether a candidate answer **is
enough** is easy. If the check is **one-directional** (values larger than an
enough value are enough too), binary search is done on the answer.

Example: boxes are loaded onto a ship in order, at most `capacity` a day. What
is the smallest capacity to finish in `days` days?

```python
def days_needed(weights, capacity):
    days, load = 1, 0
    for w in weights:
        if load + w > capacity:            # does not fit: a new day
            days, load = days + 1, 0
        load += w
    return days


def min_capacity(weights, days):
    lo, hi = max(weights), sum(weights)    # the answer is in this range
    checks = 0
    while lo < hi:
        mid = (lo + hi) // 2
        checks += 1
        if days_needed(weights, mid) <= days:
            hi = mid                       # enough: try smaller
        else:
            lo = mid + 1                   # not enough: need larger
    return lo, checks


boxes = [3, 2, 2, 4, 1, 4, 5, 3, 7, 6]
print(min_capacity(boxes, 3))
import random
random.seed(2)
big = [random.randint(1, 1000) for _ in range(100_000)]
cap, checks = min_capacity(big, 50)
print(cap, checks, sum(big) - max(big))
```

```text
(13, 5)
1000274 25 49994662
```

With a hundred thousand boxes the candidate range has about 50 million values;
trying each candidate in turn means walking the hundred thousand boxes 50
million times. Binary search found it in 25 checks: `O(n log S)`, where `S` is
the width of the range.

## Monotonic stack

"For each day, how many days until a warmer day?" The naive way looks forward
from every day: `O(n²)`. A **monotonic stack** keeps the days whose answer is
not found yet in a stack, with temperatures in decreasing order. If the new day
is warmer than the day on top of the stack, that day's answer is found: pop it.

```python
def next_warmer_slow(temps):
    result, comps = [0] * len(temps), 0
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            comps += 1
            if temps[j] > temps[i]:
                result[i] = j - i
                break
    return result, comps


def next_warmer(temps):
    result, stack, comps = [0] * len(temps), [], 0
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            comps += 1
            j = stack.pop()                # j's answer is found
            result[j] = i - j
        stack.append(i)
    return result, comps


temps = [22, 21, 23, 20, 19, 24, 25, 18]
print(next_warmer(temps)[0])
falling = list(range(5000, 0, -1)) + [9999]
print(next_warmer_slow(falling)[1], next_warmer(falling)[1])
```

```text
[2, 1, 3, 2, 1, 1, 0, 0]
12502500 5000
```

Five thousand days of steady cooling and a warm day at the end: the naive way
makes 12.5 million comparisons, the stack 5000. Since each day enters the
stack once and leaves once, it is `O(n)`. The same pattern appears in "the next
greater element", the largest rectangle in a histogram and stock price span
questions.

## BFS in a state space

In some puzzles the graph is not given explicitly: **states** are the nodes and
**moves** are the edges. Since the fewest-moves question is a shortest path in
an unweighted graph, BFS is used.

Example: measure exactly 4 litres with two buckets of 3 and 5 litres. The
moves: fill a bucket, empty it, pour from one into the other.

<figure class="fig">
<svg viewBox="0 0 540 80" width="540" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dim" d="M0 0L10 5L0 10z"/></marker></defs>
<line class="line" x1="62.0" y1="40.0" x2="86.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="140.0" y1="40.0" x2="164.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="218.0" y1="40.0" x2="242.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="296.0" y1="40.0" x2="320.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="374.0" y1="40.0" x2="398.0" y2="40.0" marker-end="url(#arr)"/>
<line class="line" x1="452.0" y1="40.0" x2="476.0" y2="40.0" marker-end="url(#arr)"/>
<circle class="box" cx="36" cy="40" r="26"/>
<text class="ink" x="36" y="44.2" font-size="12" text-anchor="middle">0,0</text>
<circle class="box" cx="114" cy="40" r="26"/>
<text class="ink" x="114" y="44.2" font-size="12" text-anchor="middle">0,5</text>
<circle class="box" cx="192" cy="40" r="26"/>
<text class="ink" x="192" y="44.2" font-size="12" text-anchor="middle">3,2</text>
<circle class="box" cx="270" cy="40" r="26"/>
<text class="ink" x="270" y="44.2" font-size="12" text-anchor="middle">0,2</text>
<circle class="box" cx="348" cy="40" r="26"/>
<text class="ink" x="348" y="44.2" font-size="12" text-anchor="middle">2,0</text>
<circle class="box" cx="426" cy="40" r="26"/>
<text class="ink" x="426" y="44.2" font-size="12" text-anchor="middle">2,5</text>
<circle class="box" cx="504" cy="40" r="26"/>
<circle class="curve4" cx="504" cy="40" r="26"/>
<text class="ink" x="504" y="44.2" font-size="12" text-anchor="middle">3,4</text>
</svg>
<figcaption>State = (in the 3-litre, in the 5-litre). Fill the 5, pour into the 3, empty the 3, move the remaining 2 into the 3, fill the 5, top up the 3: 4 litres stay in the 5-litre.</figcaption>
</figure>

```python
from collections import deque


def jug_steps(a, b, goal):
    start = (0, 0)
    prev = {start: None}                   # both seen and the way back
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if goal in (x, y):
            path, state = [], (x, y)
            while state:
                path.append(state)
                state = prev[state]
            return path[::-1]
        pour_xy = min(x, b - y)
        pour_yx = min(y, a - x)
        for nxt in [(a, y), (x, b), (0, y), (x, 0),
                    (x - pour_xy, y + pour_xy), (x + pour_yx, y - pour_yx)]:
            if nxt not in prev:
                prev[nxt] = (x, y)
                queue.append(nxt)
    return None


print(jug_steps(3, 5, 4))
print(jug_steps(2, 4, 3))
```

```text
[(0, 0), (0, 5), (3, 2), (0, 2), (2, 0), (2, 5), (3, 4)]
None
```

Six moves; BFS guarantees there is no shorter way. With buckets of 2 and 4
litres, 3 litres is impossible: all states were visited. (With buckets, only
multiples of the gcd of the volumes can be measured; `gcd(2, 4) = 2`.)

## Meet in the middle

Trying all subsets of 36 items means `2³⁶` ≈ 69 billion subsets. **Meet in the
middle** splits the items in two: the `2¹⁸` subset sums of each half are
computed separately, one is sorted, and for each sum of the other half a
partner is found with binary search.

```python
from bisect import bisect_right


def subset_sums(items):
    sums = [0]
    for x in items:
        sums += [s + x for s in sums]      # each item: take it or not
    return sums


def count_at_most(items, limit):
    half = len(items) // 2
    left = subset_sums(items[:half])
    right = sorted(subset_sums(items[half:]))
    count = sum(bisect_right(right, limit - s) for s in left)
    return count, len(left) + len(right)


random.seed(5)
items = [random.randint(1, 1000) for _ in range(36)]
count, work = count_at_most(items, 9000)
print(count, work, 2 ** 36)
small = items[:16]
brute = sum(1 for mask in range(2 ** 16)
            if sum(small[i] for i in range(16) if mask >> i & 1) <= 4000)
print(brute, count_at_most(small, 4000)[0])
```

```text
27684403632 524288 68719476736
12718 12718
```

27.7 billion subsets with a total not above 9000 were counted by computing
only about half a million sums. The last line confirms that on 16 items, where
brute force can keep up, both ways give the same answer.

## Recognising the pattern

| If the problem has | Try |
|---|---|
| "at least / at most" + a candidate is easy to check | binary search on the answer |
| "the next greater / smaller" | a monotonic stack |
| "fewest moves", states and moves | BFS in a state space |
| `n` ~40, subsets | meet in the middle |
| subarray sums, range queries | prefix sums (Core Algorithms) |
| pairs in a sorted array, a window | two pointers, sliding window (Core Algorithms) |
| "how many ways / the best" + overlapping subproblems | dynamic programming |
| choosing the local best at each step is safe | greedy |

## In machine learning

- Binary search on the answer: the **smallest threshold** at which a model
  reaches the wanted precision, or the largest batch size that fits in memory,
  is found this way.
- Monotonic stack: "the next peak" and drawdown calculations in time series.
- Search in a state space: agents that play games and plan (the classic
  background of reinforcement learning).

## Summary

- First estimate the complexity budget from the input size.
- With a one-directional check, binary search on the answer.
- For "the next greater" questions, a monotonic stack, `O(n)`.
- For fewest-moves questions, count states as nodes and use BFS.
- At `n` ~40, split the subsets in two and meet in the middle.
