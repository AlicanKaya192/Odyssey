The skeletons you will use most, in one place.

## Two pointers (sorted list)

```python
lo, hi = 0, len(items) - 1
while lo < hi:
    total = items[lo] + items[hi]
    if total == target:
        break
    if total < target:
        lo += 1
    else:
        hi -= 1
```

## Sliding window

```python
window = sum(values[:k])                  # fixed window
best = window
for i in range(k, len(values)):
    window += values[i] - values[i - k]   # add what enters, remove what leaves
    best = max(best, window)
```

```python
left = 0                                  # variable window
for right, x in enumerate(items):
    # add x to the window
    while CONDITION_BROKEN:
        # remove items[left] from the window
        left += 1
    # right - left + 1 is the window size
```

## Prefix sums

```python
prefix = [0]
for x in values:
    prefix.append(prefix[-1] + x)
# the sum of values[lo:hi]: prefix[hi] - prefix[lo]
```

## Counting and grouping with a dictionary

```python
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1

groups = {}
for word in words:
    groups.setdefault("".join(sorted(word)), []).append(word)
```

## Stacks and queues

```python
stack = []                  # LIFO
stack.append(x); top = stack.pop()

from collections import deque
queue = deque([start])      # FIFO
while queue:
    node = queue.popleft()
```

## Recursion on a tree

```python
def solve(node):
    if node is None:
        return EMPTY_ANSWER
    return COMBINE(node.value, solve(node.left), solve(node.right))
```

## Heap

```python
import heapq
heapq.heappush(h, (priority, number, item))
priority, number, item = heapq.heappop(h)
heapq.nlargest(k, values)   # the largest k, O(n log k)
```

## The cost of Python operations

| Operation | Cost |
|---|---|
| `lst[i]`, `lst.append(x)`, `lst.pop()` | `O(1)` |
| `x in lst`, `lst.index(x)`, `lst.count(x)`, `lst.remove(x)` | `O(n)` |
| `lst.insert(0, x)`, `lst.pop(0)` | `O(n)` |
| `x in s`, `s.add(x)`, `d[k]`, `d[k] = v` | `O(1)` on average |
| `dq.appendleft(x)`, `dq.popleft()` | `O(1)` |
| `sorted(lst)`, `lst.sort()` | `O(n log n)` |
| `bisect.bisect_left(lst, x)` | `O(log n)` |
| `bisect.insort(lst, x)` | `O(n)` |
| `heapq.heappush`, `heapq.heappop` | `O(log n)` |
| `heapq.heapify(lst)` | `O(n)` |
| `min(lst)`, `max(lst)`, `sum(lst)` | `O(n)` |
| `lst[a:b]` (a slice) | `O(b - a)` |
