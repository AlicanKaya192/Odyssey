Three common patterns of binary search. In all three the region halves
every round: `O(log n)`.

## 1. Exact match

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

**Invariant:** if the target is in the list, it is always within `lo..hi`.
When the region empties (`lo > hi`), the target is missing.

## 2. The first place equal to or greater than the target (lower bound)

```python
def lower_bound(items, target):
    lo, hi = 0, len(items)          # hi = len: "none of them" is a possible answer too
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

It gives the same result as `bisect.bisect_left`. Note: in this pattern `hi`
is **not included** in the range (a half-open range), which is why the
condition `lo < hi` and `hi = mid` are right. **Do not mix** the patterns:
using one's `hi` with the other's condition skips elements, as in the
lesson, or loops forever.

## 3. Searching on the answer

For a condition where "if it holds at `k`, it holds for every larger `k`"
(or the other way round), finding where the condition flips:

```python
def first_true(lo, hi, condition):
    # condition(lo..hi) is False first, then True for good; returns the first True.
    while lo < hi:
        mid = (lo + hi) // 2
        if condition(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Examples: "How few boxes are enough?", "The largest `k` with `k * k <= n`",
"In which version did the bug start?" (git's `bisect` command is exactly
this).

## Test list

After writing a binary search, **always** try:

- An empty list, a one-element list
- **Every** value in the list (the first, the last, the ones in between)
- Values not in the list: below the smallest, above the largest, between two
  elements
- Repeated values (if the first/last occurrence is wanted)

## Computing `mid`

Integers do not overflow in Python; `(lo + hi) // 2` is safe. In languages
like Java and C, `lo + hi` can overflow when very large, so
`lo + (hi - lo) // 2` is written. In Python both give the same result.
