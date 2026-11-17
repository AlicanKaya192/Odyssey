`pairwise_sq_dist(a, b)` should give all **squared distances** between two
lists of points as a `(len(a), len(b))` table. The nested loop at the start
is correct but slow: write it **without a loop**, with broadcasting
(`a[:, None, :] - b[None, :, :]`). Return the result as a list of integers
(`.long().tolist()`).

**Expected output:**

```
[[1, 13], [4, 4]]
```
