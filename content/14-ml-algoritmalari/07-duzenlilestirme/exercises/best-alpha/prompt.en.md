Write the function `best_alpha(X, y, alphas, k)`: compute the `k`-fold
cross-validation MSE for each `α` (folds `np.array_split(np.arange(n), k)`, no
shuffling) and return the `α` with the smallest error. `ridge` is ready.

**Expected output:**

```
0.01
```
