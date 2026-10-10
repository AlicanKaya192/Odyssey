The data has two crescents and a small cluster. `hdbscan_summary(size)` should
cluster with `HDBSCAN(min_cluster_size=size, copy=True)` and return
`[cluster_count, noise_count, ARI]` (`-1` is noise, not a cluster; ARI with 3
places). The starter code uses DBSCAN with a single `eps` and ignores
`size`.

**Expected output:**

```
[3, 3, 0.991]
[3, 0, 1.0]
```
