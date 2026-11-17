`masked_mean(vectors, mask)`: `vectors` is `(B, T, D)`, `mask` is `(B, T)` (1
real, 0 padding). For each sequence take the mean of the vectors at the real
positions only, and return the `(B, D)` result as a list with 3 places.

**Expected output:**

```
[[2.0, 3.0], [2.0, 2.0]]
```
