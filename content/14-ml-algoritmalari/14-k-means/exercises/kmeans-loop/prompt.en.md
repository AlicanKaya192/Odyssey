Write the function `kmeans_loop(X, init, max_iter=100)`. Each round,
first assign the points to the nearest centroid, then move the centroids to
the means; stop if the new centroids equal the old ones (`np.allclose`).
Return `(centroids, rounds)`: the centroids `.round(3).tolist()`, the rounds
the number of times the assign step ran.

**Expected output:**

```
[[1.25, 1.5], [3.9, 5.1]]
3
```
