## The skeleton

```python
def solve(problem):
    if IS_SMALL(problem):            # base case: solve directly
        return DIRECTLY(problem)
    parts = SPLIT(problem)
    answers = [solve(p) for p in parts]
    return COMBINE(answers)
```

## Common shapes

`T(n)` means "the cost of a problem of size `n`".

| Shape | Example | Cost |
|---|---|---|
| `T(n) = T(n/2) + 1` | binary search | `O(log n)` |
| `T(n) = T(n/2) + n` | quickselect (on average) | `O(n)` |
| `T(n) = 2T(n/2) + 1` | visiting every node of a tree | `O(n)` |
| `T(n) = 2T(n/2) + n` | merge sort, maximum subarray | `O(n log n)` |
| `T(n) = 3T(n/2) + n` | Karatsuba | `O(n^1.58)` |
| `T(n) = 4T(n/2) + n` | four-piece multiplication | `O(n²)` |
| `T(n) = T(n − 1) + n` | quick sort's bad pivot | `O(n²)` |
| `T(n) = 2T(n − 1) + 1` | Towers of Hanoi | `O(2ⁿ)` |

The lesson of the last two rows: if the pieces shrink **one by one** rather
than **by half**, the gain of divide and conquer is lost.

## Computing with the tree

1. How much work is at the root? (`f(n)`)
2. How many pieces on each level, how big is each? The total work of the
   level?
3. How many levels? (`log₂ n` if it halves)
4. Add up the levels. If the levels are equal, `level work × log n`; if they
   shrink going down, the work at the root; if they grow, the number of
   leaves.

## Common mistakes

- Forgetting the base case or not shrinking the piece → endless recursion.
- Slipping in the `mid` computation: `lo..mid` and `mid+1..hi` must each hold
  at least one element; `lo..mid-1` and `mid..hi` can loop forever on two
  elements.
- Slicing the list on every call (`values[:mid]`) makes copies; on large data
  working with `lo`, `hi` indexes saves memory.
- If the pieces overlap (the same subproblem twice), look at a cache first:
  dynamic programming.
