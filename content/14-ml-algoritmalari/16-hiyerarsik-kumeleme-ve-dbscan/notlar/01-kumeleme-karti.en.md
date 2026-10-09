## Four methods side by side

| | k-Means | GMM | Hierarchical | DBSCAN |
|---|---|---|---|---|
| Cluster definition | closeness to a centre | probability distribution | merge tree | dense region |
| Needs `k`? | yes | yes (BIC) | no, cut the tree | no |
| Shape | round | ellipse | depends on linkage | free |
| Noise | every point in a cluster | every point in a cluster | single chains | label `−1` |
| Large data | fast | medium | slow (`n²` memory) | medium |

## Hierarchical: linkages

| Linkage | Distance between two clusters | Tendency |
|---|---|---|
| `single` | the two closest points | long, chained shapes; sensitive to noise |
| `complete` | the two farthest points | tight clusters of equal diameter |
| `average` | the mean over all pairs | in between |
| `ward` | the increase in the within-cluster sum of squares | like k-Means, round |

SciPy: `linkage(X, method)`, `fcluster(Z, t, criterion="distance")` cuts the
tree at height `t`, `dendrogram(Z)` draws it. scikit-learn:
`AgglomerativeClustering(n_clusters, linkage=...)`.

## DBSCAN

- Core: at least `min_samples` points (itself included) within `eps`.
- Border: a neighbour of a core point but not a core point itself.
- Noise: label `−1`.
- A starting value for `min_samples`: twice the number of features; `eps`
  from the k-distance plot.

## Common mistakes

- Not scaling: `eps` is a single distance, meaningless when units differ.
- Taking DBSCAN's noise (`−1`) for a cluster.
- Applying hierarchical clustering to hundreds of thousands of rows: the
  distance matrix needs `n²` memory.
- Using single linkage on noisy data.
