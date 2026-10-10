`silhouette_table(ks)` should return a `[k, silhouette]` row for each `k` (3
places). The clustering is done on scaled data; the silhouette must be
computed **in the same space**, that is on the data transformed by the
pipeline's first step. The starter code gives the raw `X`.

**Expected output:**

```
[2, 0.755]
[3, 0.571]
[4, 0.546]
```
