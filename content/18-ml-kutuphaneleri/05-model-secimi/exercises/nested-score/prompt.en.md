`nested(cs)` should compute two numbers on **all** the data (`X`, `y`):

- `"inner"`: the `best_score_` of `GridSearchCV(LogisticRegression(), {"C": cs},
  cv=5)`
- `"outer"`: the mean of `cross_val_score(..., cv=5)` of the same search
  (nested)

Both with 3 places. `inner` is optimistic, `outer` the honest estimate.

**Expected output:**

```
0.847 0.847
```
