## Tools

| Code | What it does |
|---|---|
| `GridSearchCV(est, {"step__setting": [...]}, cv=5)` | every combination |
| `RandomizedSearchCV(est, distributions, n_iter=30, random_state=0)` | random combinations |
| `HalvingGridSearchCV` (`from sklearn.experimental import enable_halving_search_cv`) | eliminates candidates on little data, gives the rest more |
| `scoring="f1"`, `scoring="neg_mean_absolute_error"` | the score measure |
| `n_jobs=-1` | spread over the cores |
| `refit=True` (default) | retrain on all training data with the best setting |

## Results

| Code | Gives |
|---|---|
| `search.best_params_` | the best settings |
| `search.best_score_` | their cross-validated mean (optimistic) |
| `search.best_estimator_` | the fitted best model |
| `pd.DataFrame(search.cv_results_)` | every candidate: mean, spread, rank |
| `search.score(X_test, y_test)` | a held-out test score |

## Distributions

| Code | For |
|---|---|
| `randint(2, 12)` | integers (depth, number of trees) |
| `loguniform(1e-3, 1e2)` | multiplicatively changing (`C`, `alpha`, learning rate) |
| `uniform(0, 1)` | flat between 0 and 1 |
| `np.logspace(-3, 2, 6)` | a log-scaled list in a grid |

## Rules

- The search on the training data; the test once, at the end.
- If the differences are smaller than the spread, pick the simplest setting.
- The more candidates, the more optimistic `best_score_`; report nested
  validation or a held-out test.
- Search coarse and wide first (log scale), then narrow down where it looks
  good.
