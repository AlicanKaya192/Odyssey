## The contract

| Code | What |
|---|---|
| `model = Class(setting=...)` | build; settings are hyperparameters |
| `model.fit(X, y)` | learn; returns `self`, can be chained |
| `model.predict(X)` | a prediction |
| `model.predict_proba(X)` | class probabilities |
| `model.score(X, y)` | accuracy / R² |
| `tr.fit(X)`, `tr.transform(X)`, `tr.fit_transform(X)` | a transformer |
| `model.get_params()`, `model.set_params(C=1)` | read / change settings |
| `sklearn.base.clone(model)` | an unfitted copy with the same settings |
| `model.coef_`, `scaler.mean_`, `model.classes_` | what was learned (`_` at the end) |

## Data shape

| Input | Shape |
|---|---|
| `X` | `(number of samples, number of features)`, two-dimensional |
| `y` | `(number of samples,)`, one-dimensional |
| a single feature | `x.reshape(-1, 1)` |
| a single sample | `x.reshape(1, -1)` or `[[...]]` |

## Errors

| Symptom | Cause |
|---|---|
| `NotFittedError` | `fit` was not called |
| `Expected 2D array, got 1D array` | `X` is one-dimensional |
| `X has 3 features, but ... is expecting 4` | the columns in training and prediction differ |
| A different score on every run | no `random_state` |
| A suspiciously good test score | a transformer was `fit` on all the data (leakage) |
| "90% accuracy" but the model is useless | imbalanced data; compare with a baseline |
