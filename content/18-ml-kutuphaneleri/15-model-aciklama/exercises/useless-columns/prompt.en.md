`useless_columns(threshold)` should return the names of the columns whose
permutation importance **on the test data** (`n_repeats=5`, `random_state=0`)
is below `threshold`. The starter code uses the forest's own importance
(`feature_importances_`) and misses the meaningless `row_id`.

**Expected output:**

```
['row_id', 'coin']
```
