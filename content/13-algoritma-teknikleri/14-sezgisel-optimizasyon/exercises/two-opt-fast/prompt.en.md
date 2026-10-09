Write the function `two_opt_length(pts, tour)`: it improves the tour with
2-opt and returns the final tour's length, `round(..., 1)`.

The loop is as in the lesson: `i` over `1..n−2`, `j` over `i+1..n−1`; if there
is an improvement, reverse `tour[i:j + 1]` right away and keep scanning; stop
when a full pass has no improvement. **Speed:** do not measure the tour from
scratch at each try; for
`a, b, c, d = tour[i-1], tour[i], tour[j], tour[(j+1) % n]` look only at the
difference `dist(a, c) + dist(b, d) − dist(a, b) − dist(c, d)` (an improvement
if `< -1e-9`). The last line has 300 cities.

**Expected output:**

```
14.0
1521.7
```
