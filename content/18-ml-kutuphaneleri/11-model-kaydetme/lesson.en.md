# Saving Models

You saw `joblib.dump` and `joblib.load` in the Machine Learning track: the
whole pipeline goes into one file. There were three warnings mentioned only
in words: the file does not know the version, the columns or whether its
source can be trusted. This section shows all three by **running** them and
explains what to do about each: putting information beside the model,
checking the input, compressing the file, catching a file from an old
version.

## Save information with the model

```python
import joblib
import pandas as pd
import sklearn
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=500, n_features=4, n_informative=3,
                           n_redundant=0, random_state=2)
X = pd.DataFrame(X, columns=["age", "income", "visits", "score"])
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
bundle = {"model": model, "sklearn": sklearn.__version__,
          "columns": list(X.columns), "threshold": 0.3, "cv_auc": 0.91}
joblib.dump(bundle, "churn.joblib")
loaded = joblib.load("churn.joblib")
print(sorted(loaded), loaded["sklearn"])
print(loaded["model"].feature_names_in_.tolist())
```

```text
['columns', 'cv_auc', 'model', 'sklearn', 'threshold'] 1.9.1
['age', 'income', 'visits', 'score']
```

- `joblib.dump` saves any Python object, not just a model. A dictionary puts
  these **beside** the model: the scikit-learn version it was trained with,
  the columns it expects, the chosen decision threshold, the measured score.
  Whoever opens the file six months later (maybe you) does not have to look
  for them elsewhere.
- A model trained on a DataFrame keeps the column names itself too:
  `feature_names_in_`.

## Check the input

```python
import warnings

new = X.head(3)
print(loaded["model"].predict_proba(new)[:, 1].round(3).tolist())
shuffled = new[["income", "age", "visits", "score"]]
for bad in [shuffled, new.drop(columns="score")]:
    try:
        loaded["model"].predict_proba(bad)
    except ValueError as err:
        print(str(err).splitlines()[1])
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    as_array = loaded["model"].predict_proba(new.to_numpy())[:, 1]
print(as_array.round(3).tolist(), str(caught[0].message)[:40])
```

```text
[0.991, 0.47, 0.143]
Feature names must be in the same order as they were in fit.
Feature names seen at fit time, yet now missing:
[0.991, 0.47, 0.143] X does not have valid feature names, but
```

- When the **order** of the columns changes or one is **missing**, the model
  raises an error. That is good: stopping instead of a wrong prediction.
- But given the same data as a NumPy array, it only raises a **warning**
  ("no valid feature names") and predicts. An array has no names; had the
  columns been in the wrong order, the model could not know and would
  quietly produce wrong numbers.
- The rule: always give the model a DataFrame with column names, and order
  it by your own list first: `new[bundle["columns"]]`.

## File size: compress

```python
import os
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=200, random_state=0).fit(X, y)
for level in [0, 3, 9]:
    joblib.dump(forest, f"forest{level}.joblib", compress=level)
    print(level, os.path.getsize(f"forest{level}.joblib") // 1024)
again = joblib.load("forest3.joblib")
print(bool((again.predict(X) == forest.predict(X)).all()))
```

```text
0 1254
3 261
9 216
True
```

- The 200-tree forest is 1254 KB uncompressed. With `compress=3` it is
  261 KB, less than a fifth; `9` is a little smaller (216 KB). Most of the
  gain comes at the first levels.
- Compression is lossless: the loaded forest gives the same predictions.
- Small models do not need it (the logistic pipeline on this data is under
  2 KB); it matters for tree ensembles and large models.

## Do not open a file you do not trust

```python
class Trap:
    def __reduce__(self):
        return (print, ("loading this file ran code",))


joblib.dump(Trap(), "trap.joblib")
result = joblib.load("trap.joblib")
print(result)
```

```text
loading this file ran code
None
```

- When saving an object, `joblib` (and `pickle` underneath) also writes "how
  to rebuild me". `__reduce__` can give this as a **function call**; loading
  makes that call.
- Here a harmless `print` ran. A function that deletes files or connects to
  the internet could be put in the same place; `load` runs it without
  asking.
- The rule: load only model files you made yourself or whose source you
  trust. A `.joblib` / `.pkl` file downloaded from the internet is treated
  like a program to be run.

## A file from an old version

```python
import pickle
from sklearn.exceptions import InconsistentVersionWarning

data = pickle.dumps(LogisticRegression().fit(X, y))
old_file = data.replace(sklearn.__version__.encode(), b"1.2.2")   # like an old file
with warnings.catch_warnings():
    warnings.simplefilter("error", InconsistentVersionWarning)
    try:
        pickle.loads(old_file)
    except InconsistentVersionWarning as warning:
        print(warning.estimator_name, warning.original_sklearn_version,
              warning.current_sklearn_version)
```

```text
LogisticRegression 1.2.2 1.9.1
```

- Every model object carries the scikit-learn version it was saved with. We
  imitated an old file by changing that to "1.2.2" by hand.
- Loading in a different version normally only gives a warning
  (`InconsistentVersionWarning`) and carries on; the model seems to work but
  the results may have changed.
- `simplefilter("error", ...)` turns the warning into an error: loading stops
  and the model and the versions can be read from the warning. That is the
  safe way for a model running on a server; the cure is retraining the model
  in that version or pinning the environment to the version it was trained
  with.

## Summary

- Save the model in a dictionary with the version, columns, threshold and
  score.
- Before predicting, order the columns by your own list; do not give a NumPy
  array.
- `compress=3` for large models.
- Do not load a model file you do not trust: loading is running code.
- Catch a version difference with `InconsistentVersionWarning`; do not let
  it pass quietly.
