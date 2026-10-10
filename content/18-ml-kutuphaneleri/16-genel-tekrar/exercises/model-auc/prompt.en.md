`model_auc(kind)` should return the mean AUC on the same folds (3 places) of the
logistic pipeline for `"linear"` and of `HistGradientBoostingClassifier(
random_state=0)` for `"boosting"`. Boosting needs no scaling or filling; only
the plan column is turned into numbers with `OrdinalEncoder`
(`ColumnTransformer([("cat", OrdinalEncoder(), ["plan"])],
remainder="passthrough")`). The starter code uses logistic in both cases.

**Expected output:**

```
0.777
0.72
```
