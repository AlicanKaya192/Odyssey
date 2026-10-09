Write the function `dbscan_labels(X, eps, min_samples)`: walk the points
in order; when you find an unlabelled core point, open a new cluster and grow
it through core points (border points join but do not spread). Clusters are
`0, 1...`, noise `-1`. Return the list of labels.

**Expected output:**

```
[0, 0, 0, 0, 0, 1, 1, 1, 1, -1]
```
