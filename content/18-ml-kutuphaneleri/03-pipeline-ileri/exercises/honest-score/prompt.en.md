`honest_score(seed)` generates completely random data (60 rows, 2000 columns, a
random target). The starter code selects the best 10 columns **from all the
data** and then cross-validates: a fake high score. Put the selection
(`SelectKBest(f_classif, k=10)`) in a pipeline together with the model and
return the mean of `cross_val_score(..., cv=5)` rounded to 2 places.

**Expected output:**

```
0.45
```
