## The algorithm

1. Choose `k` centroids (with k-means++).
2. **Assign:** every point to its nearest centroid.
3. **Update:** every centroid becomes the mean of its points.
4. Repeat 2–3 until the centroids stop.

One round costs `n · k · d` (points × centroids × features); it is fast even
on large data.

## Measures

| What | Definition | Good |
|---|---|---|
| Inertia | `Σ ‖x − centroid(x)‖²` | small, but always falls as `k` grows |
| Silhouette | `s = (b − a) / max(a, b)` | close to 1 |
| Adjusted Rand | found clusters vs true groups | 1 (only when labels exist) |

In the silhouette, `a` is the point's mean distance to the points of its own
cluster, `b` its mean distance to the nearest other cluster.

## scikit-learn

| Parameter | Meaning |
|---|---|
| `n_clusters` | `k` |
| `init` | `"k-means++"` (default), `"random"` or an array |
| `n_init` | how many starts; the lowest inertia is kept |
| `max_iter` | the round limit |

Results: `cluster_centers_`, `labels_`, `inertia_`, `n_iter_`; `predict` for a
new point.

## Common mistakes

- Not scaling: the feature with the large unit decides the distance alone.
- Choosing `k` where the inertia is smallest: that is always the largest `k`.
- Settling for a single start: a local minimum.
- An empty cluster: the mean of a centroid with no points cannot be computed;
  scikit-learn moves that centroid to the farthest point, and a hand-written
  version must think about it.
- Applying it to categorical data: the mean is meaningless (variants such as
  k-modes exist).
