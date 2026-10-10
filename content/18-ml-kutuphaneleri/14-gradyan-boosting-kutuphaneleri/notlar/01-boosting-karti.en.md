## The same setting, two names

| Meaning | HistGradientBoosting | LightGBM |
|---|---|---|
| number of trees | `max_iter` (100) | `n_estimators` (100) |
| learning rate | `learning_rate` (0.1) | `learning_rate` (0.1) |
| number of leaves | `max_leaf_nodes` (31) | `num_leaves` (31) |
| depth | `max_depth` (unlimited) | `max_depth` (-1, unlimited) |
| at least rows per leaf | `min_samples_leaf` (20) | `min_child_samples` (20) |
| L2 penalty | `l2_regularization` | `reg_lambda` |
| row/column sampling | none | `subsample` + `subsample_freq`, `colsample_bytree` |
| early stopping | `early_stopping="auto"`, `validation_fraction` | `eval_X`, `eval_y`, `lgb.early_stopping(n)` |
| categorical | `categorical_features="from_dtype"` | `category` dtype automatically |
| silence messages | — | `verbose=-1` |

## Attributes to read

| Attribute | What |
|---|---|
| `n_iter_` (Hist) / `best_iteration_` (LGBM) | the trees used with early stopping |
| `is_categorical_` (Hist) | which columns were treated as categorical |
| `feature_importances_` (LGBM) | split count |
| `booster_.feature_importance(importance_type="gain")` | gain |
| `evals_result_` (LGBM) | the validation loss after each tree |

## Tuning order

1. Keep the learning rate small (0.05–0.1), give many trees, let early
   stopping cut them.
2. Tune complexity: `num_leaves` / `max_leaf_nodes`, `min_child_samples`.
3. If needed, sampling and penalties (`subsample`, `colsample_bytree`,
   `reg_lambda`).
4. The whole search with cross-validation; the test once at the end.
