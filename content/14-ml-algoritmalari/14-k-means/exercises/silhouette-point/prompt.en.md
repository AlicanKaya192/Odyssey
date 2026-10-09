Write the function `silhouette_point(X, labels, i)`. `a`: the mean
(true, not squared) distance from point `i` to the **other** points of its
cluster; `b`: the smallest of its mean distances to each other cluster.
`s = (b − a) / max(a, b)`, `round(..., 3)`. Every cluster has at least two
points.

**Expected output:**

```
0.868
0.849
```
