Write the function `cv_accuracy(X, y, k)`: without shuffling, split into `k`
consecutive folds (the first `n % k` folds get one more); in each fold train
the nearest centroid model **only on the training** part and measure the
accuracy on the test part. It returns the mean of the accuracies,
`round(..., 3)`. `centroid_fit` and `centroid_predict` are ready.

**Expected output:**

```
0.917
```
