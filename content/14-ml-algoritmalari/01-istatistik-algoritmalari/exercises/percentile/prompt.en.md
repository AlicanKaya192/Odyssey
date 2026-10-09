Write the function `percentile(values, q)`: the position in the sorted list
is `(n − 1) · q / 100`; if not a whole number, linear interpolation between the
two neighbours. It returns `round(..., 2)`.

No `np.percentile`, `quantile`, `median`.

**Expected output:**

```
0 1.0
25 2.5
50 4.0
90 7.8
100 9.0
```
