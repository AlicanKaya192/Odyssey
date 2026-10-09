Write the function `auc_by_pairs(y, score)`: over all (positive, negative)
pairs, count 1 if the positive's score is higher, 0.5 if equal, 0 if lower;
return the mean, `round(..., 4)`. This is the ROC AUC itself.

No `roc_auc_score`.

**Expected output:**

```
0.75
0.5
```
