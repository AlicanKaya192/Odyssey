`time_splits(n, splits, gap)` should split a series of `n` periods with
`TimeSeriesSplit(n_splits=splits, gap=gap)`. For each fold return
`[last_training_index, test_indices]` (`int(train.max())`, `test.tolist()`).
The starter code uses `KFold`; the training contains the future.

**Expected output:**

```
[3, [4, 5]]
[5, [6, 7]]
[7, [8, 9]]
[9, [10, 11]]
```
