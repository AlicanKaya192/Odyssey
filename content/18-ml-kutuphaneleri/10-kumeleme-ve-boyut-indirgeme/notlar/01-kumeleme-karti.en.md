## Clustering

| Class | Cluster shape | Key setting | `predict` |
|---|---|---|---|
| `KMeans(n_clusters, n_init=10)` | round, similar size | `n_clusters` | yes |
| `MiniBatchKMeans(n_clusters)` | the same, very large data | `batch_size` | yes |
| `GaussianMixture(n_components)` | ellipses, probabilistic | `covariance_type` | yes |
| `AgglomerativeClustering(n_clusters, linkage)` | by linkage | `linkage` | no |
| `DBSCAN(eps, min_samples)` | any shape, one density | `eps` | no |
| `HDBSCAN(min_cluster_size)` | any shape, different densities | `min_cluster_size` | no |

## Measures

| Function | When |
|---|---|
| `adjusted_rand_score(y, labels)` | true labels exist; ignores the numbers |
| `normalized_mutual_info_score(y, labels)` | the same purpose, another measure |
| `silhouette_score(X, labels)` | no labels; in the space of the clustering |
| `model.inertia_` | KMeans; always falls as `k` grows |
| `GaussianMixture.bic(X)` | the number of components; smaller is better |

## Dimensionality reduction

| Class | What | `transform` |
|---|---|---|
| `PCA(n_components=10)` | linear, a fixed number of components | yes |
| `PCA(n_components=0.95)` | 95% of the variance | yes |
| `TruncatedSVD(n_components)` | sparse matrices (text) | yes |
| `TSNE(n_components=2)` | drawing only | no |

## Rules

- Scale before any distance-based method (`StandardScaler`).
- Cluster numbers are arbitrary; compare with ARI.
- The label `-1` (DBSCAN/HDBSCAN) is noise, not a cluster.
- Axes from PCA and t-SNE have no units.
