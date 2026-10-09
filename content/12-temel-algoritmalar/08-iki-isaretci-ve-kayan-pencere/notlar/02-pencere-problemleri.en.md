The sliding window turns up very often in data work; most of its uses have a
ready-made tool too.

## Moving average

```python
def moving_average(values, k):
    result = []
    total = 0
    for i, value in enumerate(values):
        total += value
        if i >= k:
            total -= values[i - k]          # the one leaving the window
        if i >= k - 1:
            result.append(total / k)
    return result

print(moving_average([2, 4, 6, 8, 10], 3))   # [4.0, 6.0, 8.0]
```

In pandas the same job is `series.rolling(3).mean()`; it was used a lot in
the Time Series path. This sliding idea runs inside it.

## The shortest piece with a sum of at least `target` (non-negative numbers)

```python
def shortest_at_least(values, target):
    start = 0
    total = 0
    best = None
    for end, value in enumerate(values):
        total += value
        while total >= target:                  # condition met: try shrinking
            length = end - start + 1
            if best is None or length < best:
                best = length
            total -= values[start]
            start += 1
    return best

print(shortest_at_least([2, 3, 1, 2, 4, 3], 7))   # 2  (4 + 3)
```

## The last `k` elements: `deque(maxlen=k)`

If only the last `k` events of a stream are to be kept, the `maxlen` setting
of `collections.deque` slides the window by itself:

```python
from collections import deque

last_three = deque(maxlen=3)
for event in [5, 1, 7, 3, 9]:
    last_three.append(event)
print(list(last_three))          # [7, 3, 9]
```

The time windows in the Big Data path's streaming section are the same idea
applied to time.
