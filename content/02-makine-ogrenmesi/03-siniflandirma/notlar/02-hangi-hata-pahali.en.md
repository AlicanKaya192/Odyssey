Classification has two kinds of error, and they are almost never equally
heavy. This whole note circles one question: **is a false alarm more
expensive, or a miss?**

## The two errors

| Error | What happened | What it costs |
|---|---|---|
| **False positive (FP)** | You saw something that was not there | Wasted resources, unnecessary worry |
| **False negative (FN)** | You missed something that was there | A case slips through, an intervention comes late |

Accuracy blends the two into one number and **erases** the difference. Two
models can have the same accuracy while one misses and the other cries wolf
— and that difference changes everything.

## A decision table

| Field | The expensive one | Priority | Threshold |
|---|---|---|---|
| Cancer screening | Missing a patient | Recall | Lower it |
| Fraud detection | A missed transaction | Recall | Lower it |
| Failure prediction | A machine that breaks | Recall | Lower it |
| Spam filter | Deleting a real email | Precision | Raise it |
| Content recommendation | A bad recommendation | Precision | Raise it |
| Automatic loan approval | Approving a bad loan | Precision | Raise it |
| CV screening | Rejecting a good candidate | Recall | Lower it |

**The common thread:** on one side is the cost of **missing** something, on
the other the cost of **doing unnecessary work**. Whichever is larger
chooses your measure.

## Questions to ask

**1. Can a miss be undone?**

A missed diagnosis progresses; a missed spam gets deleted and forgotten.
Errors that cannot be undone push the weight towards recall.

**2. What happens after a false alarm?**

If a human checks it, a false alarm is cheap — just time. If it triggers an
automatic action, it is expensive.

**3. Who receives the result?**

A list going to an expert can afford to be wide (recall). A decision going
straight to a user has to be clean (precision).

**4. How many positives are there?**

If ten records in a thousand are positive, raising recall brings hundreds of
false alarms. On imbalanced data the trade-off is far sharper.

## Adjusting with the threshold

The decision point can be moved without retraining:

```python
probability = model.predict_proba(X_test)[:, 1]

screening = (probability >= 0.30).astype(int)   # fewer misses
spam_filter = (probability >= 0.80).astype(int) # fewer false alarms
```

| Threshold | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Low | ↑ | ↑ | ↓ | ↓ | ↑ |
| High | ↓ | ↓ | ↑ | ↑ | ↓ |

**There is no free improvement.** Moving the threshold reduces one error and
raises the other. Real improvement only comes from a better model or better
features.

## Where the threshold is chosen

The threshold is a **hyperparameter**: it is chosen on a validation set, not
on the test set. Tuning it by looking at the test set stops the test score
from being honest.

The practical route:

1. Train the model on the training set.
2. Try many thresholds on the validation set and read off precision and
   recall.
3. Pick the threshold the problem calls for ("recall must be at least
   0.90", say).
4. Measure **once** on the test set.

## Setting a constraint

In most real projects the decision is made like this: **put a floor under
one side and optimise the other.**

- "Recall must be at least 90%, push precision as high as you can."
  → Disease screening.
- "Precision must be at least 95%, push recall as high as you can."
  → An automatic approval system.

That constraint is not a technical decision; it is settled with domain
knowledge, by talking to the people who do the work. Whoever builds the
model cannot invent the number alone.

## When F1 is enough

F1 combines precision and recall with equal weight. That is only right when
the two errors really do cost about the same.

When they do not, a weighted version is used:

```python
from sklearn.metrics import fbeta_score

fbeta_score(y_test, prediction, beta=2)     # weight towards recall
fbeta_score(y_test, prediction, beta=0.5)   # weight towards precision
```

`beta > 1` foregrounds recall, `beta < 1` precision. `beta=1` is F1 itself.

## When reporting

One number is not enough. A classification result carries:

- Precision and recall **separately** (F1 as well, if you have it)
- The four numbers of the confusion matrix
- The baseline's accuracy
- Which threshold was used
- How many records each class has (`support`)

**Writing down the threshold matters especially:** the same model produces
entirely different numbers at different thresholds, and without it the
result cannot be reproduced.
