# Gradient Boosting Libraries

You wrote the idea of gradient boosting in the ML Algorithms module: each new
tree corrects the errors of the earlier ones. On tabular data the strongest
models often come from this family. This section covers two fast
implementations: scikit-learn's `HistGradientBoostingClassifier` and a
separate package, **LightGBM**. The topics are speed, missing values and
categorical columns, early stopping, and two kinds of feature importance.

## HistGradientBoosting: speed

```python
import time
from sklearn.datasets import make_classification
from sklearn.ensemble import (GradientBoostingClassifier,
                              HistGradientBoostingClassifier)
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=20000, n_features=20, n_informative=8,
                           flip_y=0.05, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
seconds = {}
for model in [GradientBoostingClassifier(random_state=0),
              HistGradientBoostingClassifier(random_state=0)]:
    start = time.perf_counter()
    model.fit(X_train, y_train)
    seconds[type(model).__name__] = time.perf_counter() - start
    print(type(model).__name__, round(model.score(X_test, y_test), 3))
print(model.n_iter_, model.early_stopping)
old, new = seconds.values()
print(old > 10 * new)
```

```text
GradientBoostingClassifier 0.943
HistGradientBoostingClassifier 0.955
86 auto
True
```

- `HistGradientBoostingClassifier` first splits each column into at most 255
  bins (a histogram) and looks for the cut point between bins. That is much
  faster than trying every value: on this computer, with 15,000 rows, the
  old class took about 10 seconds and the new one under half a second (the
  last line: more than 10 times).
- Accuracy is better too (0.955 vs 0.943). Above 10,000 rows there is no
  reason to choose the old `GradientBoostingClassifier`.
- `early_stopping="auto"` is the default: if the data has more than 10,000
  rows, it sets aside a validation part itself and stops adding trees when
  improvement stops. Here it stopped at 86 instead of 100 (`n_iter_`).

## Missing values and a categorical column

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
names = [f"c{i}" for i in range(30)]
effect = dict(zip(names, rng.normal(0, 1, 30)))
city = rng.choice(names, 6000)
x1 = rng.normal(0, 1, 6000)
chance = 1 / (1 + np.exp(-(1.5 * pd.Series(city).map(effect) + x1)))
target = (rng.random(6000) < chance).astype(int)
df = pd.DataFrame({"city": pd.Categorical(city), "x1": x1})
df.loc[rng.random(6000) < 0.1, "x1"] = np.nan          # 10% missing
d_train, d_test, t_train, t_test = train_test_split(df, target, random_state=2)
native = HistGradientBoostingClassifier(categorical_features="from_dtype",
                                        random_state=0)
native.fit(d_train, t_train)
print(native.is_categorical_.tolist(), round(native.score(d_test, t_test), 3))
codes = HistGradientBoostingClassifier(categorical_features=None, random_state=0)
codes.fit(d_train.assign(city=d_train.city.cat.codes), t_train)
as_codes = d_test.assign(city=d_test.city.cat.codes)
print(round(codes.score(as_codes, t_test), 3))
```

```text
[True, False] 0.739
0.746
```

- A categorical column with 30 cities and a number column with 10% missing.
  The model took both **without preprocessing**: it learns a separate
  direction for `NaN`, and it recognises the `category` column as
  categorical with `categorical_features="from_dtype"` (`is_categorical_`:
  `[True, False]`).
- In a categorical split a tree can form groups like "c3, c17, c25 to one
  side, the rest to the other". Turning the cities into position numbers
  (`cat.codes`) and giving them as numbers gave almost the same score on this
  data (0.746 vs 0.739): here the gain of native support is convenience, not
  accuracy. Which one is better depends on the data; it is not assumed
  better without measuring.

## LightGBM and early stopping

```python
import lightgbm as lgb
from lightgbm import LGBMClassifier
from sklearn.metrics import log_loss

X, y = make_classification(n_samples=3000, n_features=20, n_informative=6,
                           flip_y=0.2, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
X_fit, X_val, y_fit, y_val = train_test_split(X_train, y_train, test_size=0.25,
                                              random_state=3)
settings = dict(n_estimators=2000, learning_rate=0.05, random_state=0, verbose=-1)
stopped = LGBMClassifier(**settings)
stopped.fit(X_fit, y_fit, eval_X=X_val, eval_y=y_val,
            callbacks=[lgb.early_stopping(50, verbose=False)])
full = LGBMClassifier(**settings).fit(X_fit, y_fit)
for name, model in [("stopped", stopped), ("full", full)]:
    proba = model.predict_proba(X_test)
    accuracy = model.score(X_test, y_test)
    print(name, round(accuracy, 3), round(log_loss(y_test, proba), 3))
print(stopped.best_iteration_)
```

```text
stopped 0.828 0.439
full 0.817 1.195
57
```

- LightGBM's scikit-learn interface is familiar: `LGBMClassifier(...).fit(X,
  y)`, `predict`, `predict_proba`; it fits into a pipeline and
  `GridSearchCV`. `verbose=-1` silences the training messages.
- 20% of the labels are noise. The 2000-tree model learns the noise too:
  test accuracy 0.817, log loss **1.195** (its probabilities are
  overconfident and wrong).
- Early stopping: a **validation** part separate from the training data
  (`eval_X`, `eval_y`) is measured after each tree; if it does not improve
  for 50 trees, training stops. It stopped at tree 57: accuracy 0.828, log
  loss 0.439.
- The validation part is **separate** from the test: stopping on the test
  data brings the test into training.
- **Version note:** old tutorials write `eval_set=[(X_val, y_val)]`; in this
  version it is deprecated (`LGBMDeprecationWarning`); use `eval_X` and
  `eval_y` instead.

## Two kinds of importance

```python
X, y = make_classification(n_samples=20000, n_features=20, n_informative=8,
                           flip_y=0.05, random_state=1)
model = LGBMClassifier(random_state=0, verbose=-1).fit(X, y)
split = model.feature_importances_
gain = model.booster_.feature_importance(importance_type="gain")
for i in [4, 5, 1]:
    print(i, int(split[i]), round(gain[i] / gain.sum(), 3))
```

```text
4 254 0.316
5 414 0.121
1 73 0.003
```

- LightGBM's `feature_importances_` is by default the **number of splits**:
  how many times the column was used in the trees. `gain` is how much those
  splits reduced the loss.
- The two rank differently: column 5 is in the most splits (414) but gives
  12.1% of the gain; column 4 is in fewer splits (254) but 31.6% of the gain
  is its. Column 1 is a noise column: used 73 times, gain 0.3%.
- For "which column matters?", `gain` is more meaningful; both come from the
  training data. For importance on unseen data, permutation importance (the
  Explaining Models section).

## Summary

- Above 10,000 rows use `HistGradientBoostingClassifier` or LightGBM; the
  old `GradientBoostingClassifier` is slow.
- Both take `NaN` and a `category` column without preprocessing.
- Early stopping with a separate validation part; in LightGBM `eval_X`,
  `eval_y` and `lgb.early_stopping`.
- LightGBM importance is the split count by default; `gain` is more
  meaningful.
