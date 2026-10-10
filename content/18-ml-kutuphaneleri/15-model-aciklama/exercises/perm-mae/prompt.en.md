`perm_mae(column)` should return the given column's permutation importance in
**MAE** terms instead of R² (`scoring="neg_mean_absolute_error"`) with 2
places: how many units the mean absolute error grows when the column is
shuffled.

**Expected output:**

```
42.37
13.47
```
