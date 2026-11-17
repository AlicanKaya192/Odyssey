`confusion(preds, labels, k)` should build the `k × k` confusion matrix:
`matrix[true][predicted]` goes up by one for every (prediction, label) pair.

**Expected output:**

```
[2, 0, 0]
[0, 1, 1]
[0, 1, 1]
```
