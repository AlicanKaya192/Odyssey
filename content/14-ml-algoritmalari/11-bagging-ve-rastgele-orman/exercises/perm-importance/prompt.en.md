Write the function `perm_importance(X, y, seed)`: the accuracy of the ready
`model_predict` is the base; `rng = np.random.default_rng(seed)`, for each
column `j` (in order) shuffle that column in a copy with `rng.permutation` and
compute the accuracy drop. Return the drops as a `round(..., 3)` list.

**Expected output:**

```
[0.0, 0.527, 0.0]
```
