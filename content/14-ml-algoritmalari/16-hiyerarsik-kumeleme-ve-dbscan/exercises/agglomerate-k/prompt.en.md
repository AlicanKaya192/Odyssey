Write the function `agglomerate_k(X, k)` (single linkage): every point is
a cluster; merge the two closest clusters until there are `k`. Return each
point's label; labels are `0, 1, 2...` by first appearance in point order
(the first point's cluster is 0).

**Expected output:**

```
[0, 0, 1, 1, 2, 2]
[0, 0, 0, 0, 1, 1]
```
