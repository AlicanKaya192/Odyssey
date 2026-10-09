Numbers arrive one by one from a stream, and after each new number **the
median so far** is wanted (a sensor's running median, the middle of a site's
response times). Sorting every time is `O(n log n)`; with two heaps each step
is `O(log n)`.

## The idea

Split the numbers in two:

- `low`: the smaller half, a **max-heap** (its root is the largest of the
  smaller half).
- `high`: the larger half, a **min-heap** (its root is the smallest of the
  larger half).

Keep two rules: every number in `low` is smaller than or equal to those in
`high`, and `low` has at most one element more. Then the median is read from
the roots: with an odd count the root of `low`, with an even count the
average of the two roots.

```python
import heapq

def running_median(stream):
    low, high = [], []         # low: a max-heap with minus, high: a min-heap
    out = []
    for x in stream:
        heapq.heappush(low, -x)
        heapq.heappush(high, -heapq.heappop(low))   # low's largest to high
        if len(high) > len(low):                    # balance the sizes
            heapq.heappush(low, -heapq.heappop(high))
        if len(low) > len(high):
            out.append(-low[0])
        else:
            out.append((-low[0] + high[0]) / 2)
    return out

print(running_median([5, 15, 1, 3, 8]))
```

```text
[5, 10.0, 5, 4.0, 5]
```

A check: `[5, 15]` → `10.0`, `[1, 3, 5, 15]` → `(3 + 5) / 2 = 4.0`,
`[1, 3, 5, 8, 15]` → `5`.

Because every new number first enters `low` and the largest from there moves
to `high`, the first rule holds by itself; the second step only balances the
sizes. Memory is `O(n)`, but each step is `O(log n)`.
