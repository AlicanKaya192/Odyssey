Write the function `best_threshold(x, y)`: for one feature the candidate
thresholds are the midpoints of the sorted distinct values; return the tuple
`(threshold, gini)` minimising the weighted Gini (the smaller threshold on a
tie), both `round(..., 4)`. `gini` is ready.

**Expected output:**

```
(3.5, 0.0)
(2.5, 0.0)
```
