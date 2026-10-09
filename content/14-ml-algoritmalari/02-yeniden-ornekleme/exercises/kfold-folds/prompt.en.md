Write the function `kfold_folds(n, k)`: split the indices `0..n−1` into `k`
**consecutive** folds and return each fold's test indices as a list. If `n` is
not divisible by `k`, the **first** `n % k` folds get one more sample (like
scikit-learn's `KFold`).

No `KFold`.

**Expected output:**

```
[0, 1, 2, 3]
[4, 5, 6, 7]
[8, 9, 10]
```
