A model's score alone says nothing: is 89% accuracy good? The way to know is
to compare it with a model that **learns nothing**. scikit-learn has a
ready-made class for this: `DummyClassifier` (and `DummyRegressor`).

```python
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=5, weights=[0.9],
                           random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
model = LogisticRegression().fit(X_train, y_train)
print(round(y_test.mean(), 3))
print(round(base.score(X_test, y_test), 3), round(model.score(X_test, y_test), 3))
flagged = [int(m.predict(X_test).sum()) for m in (base, model)]
print(*flagged, int(y_test.sum()))
```

```text
0.108
0.892 0.94
0 18 27
```

## What happened?

- The positive class makes up 10.8% of the test set. That is why the baseline
  that always says "0" gets **89.2%** accuracy, yet it finds not a single
  positive (the number of positives it predicts is 0).
- The real model gets 94%: only 5 points better than the baseline. It flagged
  18 of the 27 positives (some may be wrong; details in the metrics section).
- The lesson: on **imbalanced** data accuracy misleads. Every new model is
  first compared with a baseline; a model that cannot beat it has learned
  nothing.

## Kinds of baselines

| Class | `strategy` | What it does |
|---|---|---|
| `DummyClassifier` | `"most_frequent"` | always the most frequent class |
| `DummyClassifier` | `"stratified"` | random, with the class proportions |
| `DummyRegressor` | `"mean"` / `"median"` | always the mean / median |

A baseline is also a scikit-learn model: the same `fit` / `predict` / `score`
interface, the same cross-validation and metric tools.
