## Building and querying

```python
prefix = [0]
for x in values:
    prefix.append(prefix[-1] + x)      # len(prefix) == len(values) + 1

def range_sum(lo, hi):                 # values[lo:hi], hi not included
    return prefix[hi] - prefix[lo]
```

| | Cost |
|---|---|
| Building | `O(n)` time, `O(n)` memory |
| One range question | `O(1)` |
| If the data changes | rebuilding is `O(n)` (if it changes often, another structure is needed) |

## Boundary mistakes

- Without the leading `0` you need a special case for `values[0:hi]`.
- `hi` is **not included** (like Python slices). If "from lo to hi
  inclusive" is wanted, `prefix[hi + 1] - prefix[lo]`.
- An empty range (`lo == hi`) gives 0; that is right.

## Two dimensions: table sums

For rectangle sums on a grid (an image, a heat map, a sales table), let
`P[r][c]` be the sum from the top-left corner up to `(r, c)`:

```python
def build_2d(grid):
    rows, cols = len(grid), len(grid[0])
    P = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
    return P

def rect_sum(P, r1, c1, r2, c2):       # rows r1..r2-1, columns c1..c2-1
    return P[r2][c2] - P[r1][c2] - P[r2][c1] + P[r1][c1]

grid = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
P = build_2d(grid)
print(rect_sum(P, 1, 1, 3, 3))         # 5 + 6 + 8 + 9 = 28
```

The `+ P[r1][c1]` on the last line adds back the top-left corner that was
subtracted twice.

## Relatives of the same idea

- **Prefix maximum:** `best[i] = max(best[i-1], values[i])`: "the highest price
  up to this day".
- **Prefix product:** accumulating ratios (return calculations).
- **Moving sum:** `prefix[i] - prefix[i - k]`; the sliding window written
  with a prefix sum.
