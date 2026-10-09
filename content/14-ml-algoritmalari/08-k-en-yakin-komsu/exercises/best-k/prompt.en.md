Write the function `best_k(X, y, ks, folds)`: compute the `folds`-fold
cross-validation accuracy for each `k` (folds `np.array_split(np.arange(n),
folds)`, no shuffling) and return the `k` with the highest accuracy; on a tie
the **smaller** `k`. `knn_labels` is ready.

**Expected output:**

```
3
```
