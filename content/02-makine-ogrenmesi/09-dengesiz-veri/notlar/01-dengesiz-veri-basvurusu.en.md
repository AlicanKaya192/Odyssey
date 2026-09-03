## Measuring the imbalance

```python
print(y.value_counts())
print(y.mean())              # the positive rate for a binary target
```

A rough scale:

| Positive rate | Situation |
|---|---|
| 40% - 50% | Balanced; accuracy is readable |
| 10% - 40% | Mildly imbalanced; watch accuracy |
| 1% - 10% | Seriously imbalanced; accuracy misleads |
| Under 1% | Extreme; consider anomaly detection |

## `stratify` when splitting

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
```

**Mandatory** on imbalanced data. Without it the number of positives in the
test set is left to chance; with a 1% class you can even end up with a test
set holding no positives at all.

For the same reason cross validation uses `StratifiedKFold`.

## Class weight

```python
LogisticRegression(max_iter=1000, class_weight="balanced")
RandomForestClassifier(n_estimators=200, class_weight="balanced")
DecisionTreeClassifier(class_weight="balanced")
```

`"balanced"` gives each class the weight `n_samples / (n_classes *
count_of_that_class)`. It can also be written by hand:

```python
class_weight={0: 1, 1: 10}
```

The measured effect: recall 0.286 → 0.667, precision 0.75 → 0.269.

**`class_weight` is a trade setting.** It raises recall and lowers
precision. Which side is right depends on the problem's costs.

## The threshold

```python
probability = model.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

`predict()` always uses 0.5. On imbalanced data that is almost never the
right place.

The threshold sweep is done on the training or validation side; choosing a
threshold by looking at the test set is exactly the leakage of section 05.

## Metrics

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix,
                             classification_report,
                             roc_auc_score, average_precision_score)
```

| Metric | What it looks at | On imbalanced data |
|---|---|---|
| `accuracy_score` | The share got right | **Misleads** |
| `precision_score` | How much of what it called positive is right | Useful |
| `recall_score` | How many real positives were caught | Useful |
| `f1_score` | The harmonic mean of the two | Useful |
| `roc_auc_score` | Ranking ability | **Optimistic** |
| `average_precision_score` | The area under the PR curve | The most sensitive |

The baselines:

| Metric | A random model's value |
|---|---|
| Accuracy | The most frequent class's share (0.944 here) |
| ROC AUC | 0.5 |
| Average precision | The positive rate (0.056 here) |

## The confusion matrix

```python
print(confusion_matrix(y_test, prediction))
# [[352   2]     TN=352  FP=2
#  [ 15   6]]    FN=15   TP=6
```

Rows are truth, columns are predictions. The diagonal from top left to
bottom right holds what was got right.

It is looked at **always** on imbalanced data: everything a single accuracy
number hides sits here.

## Choosing a metric in cross validation

```python
cross_val_score(model, X_train, y_train, cv=skf, scoring="average_precision")
```

Common `scoring` values: `"accuracy"`, `"precision"`, `"recall"`, `"f1"`,
`"roc_auc"`, `"average_precision"`, `"balanced_accuracy"`.

The measured spreads: `accuracy` 0.008, `recall` 0.188, `roc_auc` 0.028,
`average_precision` 0.144. A metric whose spread is near zero cannot choose
a hyperparameter.

## Resampling

Not in sklearn; it lives in `imbalanced-learn`:

```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
```

Three rules:

1. Apply it **to the training set only**.
2. In cross validation do it **inside each fold**, not before.
3. `class_weight` does the same job in most cases without touching the
   data; try it first.

## Common mistakes

- **Reporting accuracy.** 94.4% is the score of a model that does nothing.
- **Forgetting `stratify`.** The number of positives in the test set is left
  to chance.
- **Writing ROC AUC alone.** It is optimistic on imbalanced data; average
  precision should be given too.
- **Choosing the threshold by looking at the test set.** Leakage.
- **Resampling before splitting.** Copies of the same row land in both
  training and test — the sneakiest form of section 04's leakage.
- **Saying `class_weight="balanced"` and calling it done.** A decision made
  without seeing how far precision fell is incomplete.
- **Comparing average precision against a 0.5 baseline.** Its baseline is
  the positive rate, here 0.056.
