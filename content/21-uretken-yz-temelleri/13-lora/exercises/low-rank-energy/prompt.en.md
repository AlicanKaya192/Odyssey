`energy(matrix, r)` should return the share of the first `r` squared singular
values in the total (`np.linalg.svd(..., compute_uv=False)`), as a `float`
rounded to 3 places.

**Expected output:**

```
1 0.878
2 0.976
3 1.0
```
