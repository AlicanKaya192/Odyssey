Write the function `farthest_first(X, k)`: a version of k-means++
without randomness. The first centroid is point 0; then each time add the
point **farthest** from its nearest chosen centroid (ties: the smaller
index). Return the indices of the chosen points as a list.

**Expected output:**

```
[0, 5, 2]
[0, 5, 2, 4]
```
