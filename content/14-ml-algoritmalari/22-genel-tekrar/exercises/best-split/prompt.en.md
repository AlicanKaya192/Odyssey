Write the function `best_split(x, y)`: one numeric feature `x`, classes
`y`. Try the midpoints of consecutive **distinct** sorted values as
thresholds; `x <= threshold` goes left, the rest right. Return the threshold
with the smallest weighted Gini impurity and the impurity as
`(threshold, round(gini, 3))`; on ties the smaller threshold.
`Gini = 1 − Σ pₖ²`.

**Expected output:**

```
(3.5, 0.0)
(1.5, 0.333)
```
