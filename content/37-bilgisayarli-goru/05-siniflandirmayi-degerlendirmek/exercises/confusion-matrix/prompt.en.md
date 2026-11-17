`confusion(y_true, y_pred, k)` should return a confusion matrix for `k`
classes (row true, column predicted) as a nested list. You can use the
lesson's `torch.bincount` approach.

**Expected output:**

```
[1, 1, 0]
[0, 2, 0]
[1, 0, 1]
```
