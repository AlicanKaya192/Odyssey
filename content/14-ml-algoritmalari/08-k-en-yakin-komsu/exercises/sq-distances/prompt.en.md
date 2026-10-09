Write the function `sq_distances(A, B)`: it returns the **squared** Euclidean
distance between each row of `A` and each row of `B` as a `(len(A), len(B))`
matrix (`.round(4).tolist()`).

No loops: broadcasting `A[:, None, :] − B[None, :, :]`.

**Expected output:**

```
[[1.0, 25.0, 0.0], [1.0, 13.0, 2.0]]
```
