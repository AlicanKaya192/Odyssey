## Tools

| Code | Its question |
|---|---|
| `permutation_importance(m, X_test, y_test, n_repeats=10)` | how much does a column help? |
| `... scoring="neg_mean_absolute_error"` | importance with another measure |
| `r.importances_mean`, `r.importances_std` | the mean drop, the spread |
| `partial_dependence(m, X, ["col"])` | the average prediction as the column changes |
| `partial_dependence(..., kind="individual")` | each row's own curve (ICE) |
| `PartialDependenceDisplay.from_estimator(m, X, ["a", "b"])` | drawing |
| `... kind="both", subsample=60` | the average + curves of sample rows |
| `PartialDependenceDisplay.from_estimator(m, X, [("a", "b")])` | the joint effect of two columns |

## Which importance?

| Importance | From | Weakness |
|---|---|---|
| `feature_importances_` (tree) | purity gain in training | favours many-valued columns |
| LightGBM `gain` | loss reduction in training | from the training data |
| `coef_` (linear) | the coefficient | depends on scale |
| permutation (test) | score drop on unseen data | split between related columns |

## Rules

- Compute permutation importance on the **test** data; on training data it
  counts memorisation as importance too.
- Turn an integer column into `float` before partial dependence.
- Find related columns (correlation, VIF) first; interpret their importances
  together.
- The model shows what it looks at; cause and effect needs an experiment.
