`leaf_table(sizes)` should build `DecisionTreeClassifier(min_samples_leaf=size,
random_state=0)` for each size and return a `[size, leaf_count, cv_score]`
row (5-fold mean, 3 places). The starter code forgets to give `size` to the
model.

**Expected output:**

```
[1, 48, 0.82]
[10, 22, 0.851]
[30, 10, 0.838]
```
