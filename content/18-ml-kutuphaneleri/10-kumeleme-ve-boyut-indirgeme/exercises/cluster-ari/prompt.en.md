`cluster_ari(k)` clusters the scaled data with `KMeans(n_clusters=k, n_init=10,
random_state=0)`. It should return the **ARI** comparing the clustering with
the true labels (`y`) with 3 places. The starter code computes accuracy;
since cluster numbers are arbitrary, accuracy is meaningless.

**Expected output:**

```
0.923
0.57
```
