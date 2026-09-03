Every measure is derived from four numbers. Knowing the confusion matrix
saves you from memorising the rest.

## The confusion matrix

```python
from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(y_test, prediction).ravel()
```

| Short | Actual | Predicted | In words |
|---|---|---|---|
| TN | 0 | 0 | True negative |
| FP | 0 | 1 | False positive — **a false alarm** |
| FN | 1 | 0 | False negative — **a miss** |
| TP | 1 | 1 | True positive |

sklearn returns the matrix in the order `[[TN, FP], [FN, TP]]`: **rows are
actual, columns predicted.** The top-left corner is always TN.

`ravel()` flattens the matrix into a list so it can be unpacked into four
variables on one line.

## The measures and their formulas

| Measure | Formula | The question it answers |
|---|---|---|
| Accuracy | `(TP + TN) / total` | How many did I get right? |
| Precision | `TP / (TP + FP)` | Of those I called 1, how many really are? |
| Recall | `TP / (TP + FN)` | Of the real 1s, how many did I find? |
| Specificity | `TN / (TN + FP)` | Of the real 0s, how many did I find? |
| F1 | `2PR / (P + R)` | The balance of precision and recall |

**Telling them apart by the denominator:**

- Precision's denominator is **your predictions**.
- Recall's denominator is **what actually exists**.

## The code

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

accuracy_score(y_test, prediction)
precision_score(y_test, prediction)
recall_score(y_test, prediction)
f1_score(y_test, prediction)
print(classification_report(y_test, prediction))
```

`classification_report` gives all of them **per class**, which is far more
informative than looking at one number.

**`zero_division`:** if no positive prediction was made, precision's
denominator is zero. sklearn warns and returns 0; writing `zero_division=0`
silences the warning.

## Which one when

| Situation | The measure to look at |
|---|---|
| Balanced classes, errors equally costly | Accuracy |
| Missing is expensive (disease, fraud) | **Recall** |
| A false alarm is expensive (spam, recommendations) | **Precision** |
| Both matter and one number is needed | F1 |
| The classes are very imbalanced | Precision + recall + confusion matrix |
| Evaluation independent of threshold | ROC-AUC |

**Accuracy alone is reliable only when the classes are balanced.** When they
are not, the baseline is already high and the number says nothing.

## The baseline

```python
most_common = y_train.mode()[0]
baseline = accuracy_score(y_test, [most_common] * len(y_test))
```

sklearn's ready-made one:

```python
from sklearn.dummy import DummyClassifier

dummy = DummyClassifier(strategy="most_frequent")
dummy.fit(X_train, y_train)
print(accuracy_score(y_test, dummy.predict(X_test)))
```

`strategy` options: `most_frequent`, `stratified` (random, following the
class proportions), `uniform` (uniformly random), `constant` (a class you
name).

## The threshold

```python
probability = model.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.4).astype(int)
```

`predict_proba` returns one column per class; `[:, 1]` is the positive
class's probability.

| Threshold | Effect |
|---|---|
| Lower it | Recall ↑, precision ↓, more false alarms |
| Raise it | Precision ↑, recall ↓, more misses |

**0.5 is not the result of a calculation but a default.** It can be changed
without retraining, and in most real problems it should be.

Choosing a threshold is choosing a hyperparameter: it is done on a
**validation** set, not on the test set.

## Multiclass problems

With more than two classes, precision and recall are computed per class and
then averaged:

| Average | How |
|---|---|
| `macro` | The mean over classes; every class weighs the same |
| `weighted` | Weighted by the number of records |
| `micro` | All TP/FP/FNs pooled into one computation |

```python
f1_score(y_test, prediction, average="macro")
```

On imbalanced data `macro` and `weighted` come out very differently:
`weighted` foregrounds the large class's success, `macro` the small class's
failure.

## Common mistakes

- **Trying to move the threshold with `predict` instead of
  `predict_proba`.** `predict` already returns 0/1; a threshold needs the
  probability.
- **Taking the wrong column from `predict_proba`.** `[:, 0]` is the negative
  class's probability, `[:, 1]` the positive one's.
- **Using a regression measure.** MAE is meaningless with a categorical
  target.
- **Skipping the baseline.** On imbalanced data 90% accuracy may not be an
  achievement at all.
- **Reversing the arguments.** The order is again `(actual, predicted)`;
  reversed, precision and recall swap places and no error is raised.
