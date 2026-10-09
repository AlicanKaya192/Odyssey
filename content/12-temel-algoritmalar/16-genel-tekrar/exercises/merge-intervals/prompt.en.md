Write the function `merge_intervals(intervals)`: it merges the `[start, end]`
intervals that **overlap or touch** and returns the result sorted by start.
The input is not sorted.

- `[[8, 10], [1, 3], [2, 6], [15, 18]]` → `[[1, 6], [8, 10], [15, 18]]`
- `[[1, 4], [4, 5]]` → `[[1, 5]]` (they touch at 4)

First sort by start (`sorted` is allowed); then in a single pass compare with
the last merged interval.

**Expected output:**

```
[[1, 6], [8, 10], [15, 18]]
[[1, 5]]
[]
```
