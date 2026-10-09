Write the function `lis_length(values)` in `O(n log n)`: it returns the length
of the longest **strictly increasing** subsequence.

Keep a `tails` list; for each `x`, `k = bisect.bisect_left(tails, x)`. If `k`
is the end of the list, append `x`, otherwise `tails[k] = x`. The answer is
`len(tails)`.

The last line has 200,000 elements; an `O(n²)` solution hits the time limit.

**Expected output:**

```
4
1
511
```
