`pipe_search(ks, cs)` should search `k` and `C` together on
`make_pipeline(StandardScaler(), SelectKBest(f_classif), LogisticRegression())`
(`cv=5`, on the training data). The grid keys must have the form
`step__setting`. Return:

- `"params"`: `[best_k, best_C]`
- `"test"`: the best model's test score, 3 places

The starter code writes the keys as `"k"` and `"C"` and fails.

**Expected output:**

```
[8, 0.1]
0.893
```
