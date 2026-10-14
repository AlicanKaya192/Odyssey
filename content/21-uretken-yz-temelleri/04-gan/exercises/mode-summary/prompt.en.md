`mode_summary(points)` should take a list of 2-dimensional points. Find
each point's distance to its nearest `CENTRES` centre; if the distance is
below 0.3, count the point towards that cluster. Return `[number of clusters
with at least one point, share of points counted towards a cluster]`; the
share a `float` rounded to 3 places.

**Expected output:**

```
[5, 0.8]
```
