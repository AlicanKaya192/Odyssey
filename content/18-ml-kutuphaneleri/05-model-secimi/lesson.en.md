# Hyperparameter Search

What should `C` be, how many columns should be selected, how deep should a
tree be? There is no formula that learns these hyperparameters from data; they
are tried and compared with cross-validation. `GridSearchCV` tries every given
combination, `RandomizedSearchCV` a random part of them. This section shows
both, how to read the results table, and that the search itself is
**optimistic**: the best score comes out higher than the true success.

## GridSearchCV and a pipeline

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=600, n_features=20, n_informative=5,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif), LogisticRegression())
grid = {"selectkbest__k": [3, 5, 10, 20], "logisticregression__C": [0.01, 0.1, 1.0]}
search = GridSearchCV(pipe, grid, cv=5).fit(X_train, y_train)
print(search.best_params_)
print(round(search.best_score_, 3), round(search.score(X_test, y_test), 3))
print(len(search.cv_results_["params"]))
```

```text
{'logisticregression__C': 1.0, 'selectkbest__k': 5}
0.853 0.867
12
```

- The grid is a dictionary: the key is `step__setting`, the value the list to
  try. 4 × 3 = 12 combinations, each with 5-fold cross-validation: 60
  trainings.
- The whole search happens on the **training** data; the test data is used
  once, at the end. `search.score(X_test, y_test)` is computed with the model
  retrained on all the training data with the best setting (`refit=True`, the
  default).
- `best_params_` is the best combination, `best_score_` its cross-validated
  mean. The fitted best model is `search.best_estimator_`.

## Reading the results table

```python
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split

X, y = make_classification(n_samples=600, n_features=20, n_informative=5,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
grid = {"C": [0.001, 0.01, 0.1, 1.0, 10.0]}
search = GridSearchCV(LogisticRegression(), grid, cv=5).fit(X_train, y_train)
cols = ["param_C", "mean_test_score", "std_test_score", "rank_test_score"]
print(pd.DataFrame(search.cv_results_)[cols].round(3).to_string(index=False))
```

```text
 param_C  mean_test_score  std_test_score  rank_test_score
   0.001            0.824           0.041                5
   0.010            0.844           0.043                1
   0.100            0.842           0.040                3
   1.000            0.842           0.037                3
  10.000            0.844           0.035                1
```

- `cv_results_` gives each combination's mean score, its spread across folds
  and its rank. It reads well as a DataFrame.
- The real lesson is in this table: the means of all `C` values from 0.01 to
  10 lie between 0.842 and 0.844, while the spread is 0.04. The differences
  are **smaller than the noise**. A "best" `C` was chosen, but with another
  seed another one could have been.
- In such a flat table it is safer to pick the simplest (most regularising)
  setting; only 0.001 is clearly worse.

## RandomizedSearchCV

```python
from scipy.stats import loguniform, randint
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split

X, y = make_classification(n_samples=600, n_features=20, n_informative=5,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
space = {"n_estimators": randint(20, 200), "max_depth": randint(2, 12),
         "min_samples_leaf": randint(1, 20), "max_features": loguniform(0.1, 1.0)}
search = RandomizedSearchCV(RandomForestClassifier(random_state=10), space,
                            n_iter=15, cv=3, random_state=10).fit(X_train, y_train)
print(sorted(search.best_params_), round(search.best_score_, 3))
print(round(search.score(X_test, y_test), 3))
```

```text
['max_depth', 'max_features', 'min_samples_leaf', 'n_estimators'] 0.862
0.927
```

- Even 5 values for each of four settings make 625 combinations. A random
  search tries `n_iter` (15) random combinations instead.
- A **distribution** can be given instead of a list: `randint(2, 12)` for
  integers, `loguniform(0.1, 1.0)` is the right range for ratios and settings
  like `C` whose scale changes multiplicatively (the step from 0.1 to 0.2
  matters as much as from 0.9 to 1.0).
- Most settings affect the result little; with the same budget a random search
  tries more distinct values of the important setting. For models with many
  settings it is more efficient than a grid.

## The search's optimism

```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(11)
X = rng.normal(size=(120, 30))
y = rng.integers(0, 2, 120)
pipe = make_pipeline(SelectKBest(f_classif), LogisticRegression())
grid = {"selectkbest__k": list(range(1, 31)),
        "logisticregression__C": np.logspace(-3, 2, 10).tolist()}
search = GridSearchCV(pipe, grid, cv=5).fit(X, y)
print(len(search.cv_results_["params"]), round(search.best_score_, 3))
outer = cross_val_score(GridSearchCV(pipe, grid, cv=5), X, y, cv=5)
print(round(outer.mean(), 3))
```

```text
300 0.642
0.517
```

- The data is **completely random** again. 300 combinations were tried and the
  best one's cross-validated score came out at 0.642. The selection is right,
  there is no leakage; but we picked **the luckiest** among 300 candidates.
  That is why `best_score_` is optimistic.
- The honest measure is **nested cross-validation**: the search itself runs
  inside an outer cross-validation; each outer fold's test data never sees the
  search. The result is 0.517: equal to chance, that is, the truth.
- The more candidates, the larger the optimism. A report states not
  `best_score_` but a held-out test score or nested validation.

## Summary

- `GridSearchCV(pipe, {"step__setting": [...]}, cv=5)` tries every
  combination; `RandomizedSearchCV(..., n_iter=)` samples from distributions.
- The search on the training data, the test once and at the end; `refit`
  retrains with the best setting.
- In `cv_results_` look at the **spread** as much as the mean: if the
  differences are smaller than the noise, pick the simple one.
- `best_score_` is optimistic; for an honest estimate, a held-out test or
  nested cross-validation.
