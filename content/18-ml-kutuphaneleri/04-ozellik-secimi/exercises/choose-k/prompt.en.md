`choose_k(ks)` should build `make_pipeline(SelectKBest(f_classif, k=k),
LogisticRegression())` for each `k` and compute the mean of
`cross_val_score(..., cv=5)`. Return:

- `"scores"`: the scores as a list in the order of `ks` (3 places)
- `"best"`: the `k` with the highest score (the smaller one on a tie)

The selection must be inside the pipeline.

**Expected output:**

```
[0.868, 0.87, 0.852]
4
```
