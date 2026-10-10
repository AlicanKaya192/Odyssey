## A model's path

1. Split the data: `train_test_split(..., stratify=y)`; the test stays until
   the end.
2. Build the preprocessing: `ColumnTransformer` + `make_pipeline`;
   everything that learns goes inside.
3. Choose the validation: `StratifiedKFold(shuffle=True)`, `GroupKFold` if
   there are groups, `TimeSeriesSplit` if there is time.
4. Choose the measure: a `scoring` that fits the task's cost; `make_scorer`
   if needed.
5. Start with a baseline: a linear model; then trees / boosting.
6. Search: `GridSearchCV` / `RandomizedSearchCV`; if differences are smaller
   than the spread, pick the simple one.
7. Choose the threshold: `TunedThresholdClassifierCV`.
8. Measure once on the test; this number goes in the report.
9. Explain: permutation importance, partial dependence + ICE.
10. Save: model + version + columns + threshold, `compress=3`.

## Common mistakes and their sections

| Mistake | Section |
|---|---|
| Fitting the scaler on all the data | The scikit-learn API, Pipelines |
| A column silently lost to `remainder="drop"` | ColumnTransformer |
| Feature selection outside the pipeline | Feature Selection |
| Reporting `best_score_` | Hyperparameter Search |
| Splitting sorted data unshuffled, `KFold` on grouped data | Validation Tools |
| Giving `predict` to AUC, choosing the threshold on the test | Metrics and Scorers |
| Silencing a `ConvergenceWarning` with `max_iter` | Linear Models |
| Trusting `feature_importances_` | Tree and Ensemble Models |
| Computing accuracy with cluster numbers | Clustering and Dimensionality Reduction |
| Loading a model file you do not trust | Saving Models |
| Forgetting `add_constant` | statsmodels: OLS |
| Forgetting the `offset` in Poisson | statsmodels: GLMs and Formulas |
| Early stopping on the test data | Gradient Boosting Libraries |
| Partial dependence on an integer column | Explaining Models |

## Changed in this version (different in old tutorials)

| Old code | In this version |
|---|---|
| `LogisticRegression(penalty="l1")` | `l1_ratio=1, solver="saga"` |
| `LogisticRegression(penalty=None)` | `C=np.inf` |
| LightGBM `fit(eval_set=[(X, y)])` | `fit(eval_X=X, eval_y=y)` |
| `HDBSCAN(...)` warning | write `copy=True` |
