# Metrics and Scorers

You met measures like MAE, F1 and AUC in the Machine Learning track. This
section looks at their **use** in scikit-learn: what happens when you write
`scoring=`, why some scores come out negative, how F1 is averaged over many
classes, why AUC must be given probabilities, how to give your own measure
(for example the **cost** of an error) to the tools, and how to choose the
decision threshold in the right place.

## scoring= and the minus sign

```python
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import get_scorer_names
from sklearn.model_selection import cross_val_score

print(len(get_scorer_names()))
X, y = make_regression(n_samples=200, n_features=4, noise=20, random_state=1)
scores = cross_val_score(LinearRegression(), X, y, cv=5,
                         scoring="neg_mean_absolute_error")
print(scores.round(1))
print(round(-scores.mean(), 2))
```

```text
58
[-12.8 -14.  -15.3 -14.1 -14.9]
14.22
```

- `scoring=` takes a **name**; `get_scorer_names()` lists them all (58 in
  this version). The same name works in `cross_val_score`, `cross_validate`,
  `GridSearchCV` and `learning_curve`.
- scikit-learn's rule: **a larger score is better**. A search picks "the
  largest". Error measures, where smaller is better, have negated versions:
  `neg_mean_absolute_error`, `neg_root_mean_squared_error`, `neg_log_loss`.
- The minus sign is not shown in a report: take the negative of the mean.
  MAE 14.22.

## Averaging over many classes

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=8, n_informative=5,
                           n_classes=3, weights=[0.7, 0.2, 0.1], random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3,
                                                    stratify=y)
pred = LogisticRegression().fit(X_train, y_train).predict(X_test)
for avg in [None, "macro", "weighted", "micro"]:
    print(avg, np.round(f1_score(y_test, pred, average=avg), 3))
print(classification_report(y_test, pred, digits=3))
```

```text
None [0.886 0.488 0.341]
macro 0.572
weighted 0.752
micro 0.776
              precision    recall  f1-score   support

           0      0.827     0.954     0.886       175
           1      0.625     0.400     0.488        50
           2      0.438     0.280     0.341        25

    accuracy                          0.776       250
   macro avg      0.630     0.545     0.572       250
weighted avg      0.747     0.776     0.752       250
```

- With more than two classes each class has its own F1 (`average=None`):
  the majority class 0.886, the smallest class 0.341.
- `macro`: the plain mean of the classes (0.572). A small class counts as
  much as a big one; missing the small class lowers this number.
- `weighted`: weighted by class size (0.752). The majority class dominates;
  it hides how bad the small classes are.
- `micro`: all predictions in one pool (0.776); for single-label multiclass
  it equals accuracy (`accuracy 0.776`).
- As scorer names: `"f1_macro"`, `"f1_weighted"`, `"recall_macro"`.
  `classification_report(..., output_dict=True)` gives the same table as a
  dictionary.

## AUC needs probabilities

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.95], flip_y=0.02, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7,
                                                    stratify=y)
model = LogisticRegression().fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
pred = model.predict(X_test)
auc_pred = roc_auc_score(y_test, pred)
auc_proba = roc_auc_score(y_test, proba)
print(round(auc_pred, 3), round(auc_proba, 3))
print(round(average_precision_score(y_test, proba), 3), round(y_test.mean(), 3))
```

```text
0.599 0.776
0.433 0.06
```

- AUC is how well the model **ranks** positives ahead of negatives; that
  needs a sortable score. `predict` gives only 0/1: AUC came out 0.599. With
  the same model's probability, 0.776.
- `roc_auc_score(y, pred)` does not fail; it quietly gives a wrong number.
  Always give AUC `predict_proba(X)[:, 1]` (or `decision_function`).
  `scoring="roc_auc"` does this by itself.
- With 6% positives `average_precision` (the area under the
  precision–recall curve) is more honest: a random model gets 0.06, this
  model 0.433. AUC's floor of 0.5 makes it easy to look good on a rare class.

## make_scorer: your own measure

Suppose in this data **missing** a positive (a false negative) costs 10 units
and a false alarm (a false positive) 1 unit. Accuracy or F1 does not know
this; we write the cost ourselves:

```python
from sklearn.metrics import confusion_matrix, make_scorer
from sklearn.model_selection import cross_val_score


def cost(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp * 1 + fn * 10


scorer = make_scorer(cost, greater_is_better=False)
print(cost(y_test, pred), scorer(model, X_test, y_test))
for weight in [None, "balanced"]:
    m = LogisticRegression(class_weight=weight)
    scores = cross_val_score(m, X_train, y_train, cv=5, scoring=scorer)
    print(weight, round(-scores.mean(), 1))
```

```text
241 -241
None 113.6
balanced 94.8
```

- The measure function takes `(y_true, y_pred)` and returns a number.
  `make_scorer` turns it into the form `scorer(model, X, y)`; now it can be
  given wherever `scoring=` goes.
- `greater_is_better=False`: the cost should be small, so the scorer returns
  it **negated** (−241). The search still picks "the largest", that is the
  cheapest.
- Two models can be compared with this measure: `class_weight="balanced"`
  cut the mean cost per fold from 113.6 to 94.8.

## Choosing the decision threshold in the right place

`predict` cuts the probability at 0.5. If the costs are unequal, 0.5 is not
the right threshold:

```python
import numpy as np
from sklearn.model_selection import TunedThresholdClassifierCV

for t in [0.5, 0.2, 0.1, 0.05]:
    print(t, cost(y_test, (proba >= t).astype(int)))
tuned = TunedThresholdClassifierCV(LogisticRegression(), scoring=scorer, cv=5)
tuned.fit(X_train, y_train)
print(round(tuned.best_threshold_, 3), cost(y_test, tuned.predict(X_test)))
```

```text
0.5 241
0.2 202
0.1 161
0.05 181
0.181 207
```

- As the threshold drops, fewer positives are missed and more false alarms
  appear. On the test data the cheapest is 0.1 (161). But choosing the
  threshold **by looking at the test data** brings the test data into
  training; that 161 is optimistic.
- `TunedThresholdClassifierCV` chooses the threshold **on the training
  data**, with cross-validation and by the given scorer: 0.181. The test cost
  fell from 241 to 207. That is the honest number.
- To fix a threshold by hand, `FixedThresholdClassifier(model,
  threshold=0.2)`; both change `predict`, `predict_proba` stays the same.

## Several measures in a search

```python
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(LogisticRegression(), {"C": [0.01, 0.1, 1, 10]}, cv=5,
                      scoring={"auc": "roc_auc", "ap": "average_precision"},
                      refit="ap").fit(X_train, y_train)
print(search.best_params_, round(search.best_score_, 3))
print(sorted(k for k in search.cv_results_ if k.startswith("mean_test")))
```

```text
{'C': 10} 0.599
['mean_test_ap', 'mean_test_auc']
```

- `scoring=` can be a dictionary: each measure enters `cv_results_` as its
  own column (`mean_test_auc`, `mean_test_ap`).
- With several measures the search cannot know which one decides "best":
  say it with `refit="ap"`. `best_score_` is that measure's value.

## Summary

- `scoring=` takes a name; larger is better, errors are negated with `neg_`.
- `average` over many classes: `macro` protects the small class, `weighted`
  hides it.
- AUC and average precision need probabilities; do not give `predict`.
- If the task has its own cost, `make_scorer(..., greater_is_better=False)`.
- The threshold is chosen not on the test data but on the training data with
  `TunedThresholdClassifierCV`.
