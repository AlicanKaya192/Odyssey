# Imbalanced Data

In section 03 you saw that accuracy alone is not enough: 85% accuracy was
not so impressive when the baseline stood at 67.5%. But there the classes
were roughly balanced.

In this section one class is **5.7%**. And there accuracy is not merely
insufficient — it is **actively misleading**.

The data is 1500 card transactions: `amount`, `hour`, `attempts` (how many
tries that day) and the target `fraud`. Of the 1500 rows, **85** are fraud.

## The model that does nothing

Set the baseline: say "not fraud" to everything.

```python
zeros = [0] * len(y_test)
print(accuracy_score(y_test, zeros))   # 0.944
```

**94.4% accuracy.** Without writing a single line of model code.

Seeing that number in a presentation would impress you. Yet the model
catches no fraud at all — not one. Its product value is **zero**.

Now build the real model:

```python
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
prediction = model.predict(X_test_scaled)

print(accuracy_score(y_test, prediction))   # 0.955
```

**95.5%.** A 1.1 point gain over the baseline. Did the model learn anything?

## The confusion matrix answers

```python
print(confusion_matrix(y_test, prediction))
# [[352   2]
#  [ 15   6]]
```

The test set holds 21 frauds. The model caught **6** and missed **15**.

```python
print(precision_score(y_test, prediction))   # 0.75
print(recall_score(y_test, prediction))      # 0.286
```

Precision is 0.75 — three quarters of what it calls fraud really is. Recall
is **0.286** — only 28.6% of the real frauds were caught.

**The gap between 0.955 and 0.944 in accuracy is almost nothing; the gap
between 0 and 0.286 in recall is everything.** Comparing two models by
accuracy means missing the only real difference between them.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Accuracy: 0.944 → 0.955</h4>
      <p>A 1.1 point rise. On a chart it would look like a flat line.</p>
    </div>
    <div class="versus-side">
      <h4>Recall: 0.000 → 0.286</h4>
      <p>From nothing to catching six. The only difference the product feels.</p>
    </div>
  </div>
  <figcaption>The same two models, the same test set. Whoever picks the metric picks the result.</figcaption>
</figure>

## Why this happens

The model is not being lazy on purpose. During training it tries to reduce
**total error**, and 1068 of the 1125 rows it holds are negative.

Getting a negative wrong spoils a group of 1068 rows; missing a positive
spoils a group of 57. Mathematically, being cautious pays: the strategy
**"say negative unless you are sure"** genuinely lowers the error.

The problem is not in the model but in the question we asked it. We said
"reduce total error", while what we wanted was "catch the frauds".

## First remedy: weighting the classes

There is a way to tell the model that missing a positive costs more than
getting a negative wrong:

```python
model = LogisticRegression(max_iter=1000, class_weight="balanced")
```

`"balanced"` gives each class a weight in inverse proportion to its
frequency. Because positives are eighteen times rarer, one positive mistake
counts eighteen times as heavy.

The measured result:

| | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Default | 0.955 | 0.750 | 0.286 | 0.414 |
| `balanced` | 0.880 | 0.269 | 0.667 | 0.384 |

**Recall rose from 0.286 to 0.667** — 14 frauds caught instead of 6.

**The cost is plain:** precision fell from 0.75 to 0.269. The model calls 52
transactions fraud, 38 of them false alarms. Accuracy dropped from 0.955 to
0.880 too.

This is a **trade**, not an improvement. Which side is right depends on the
problem itself: is a missed fraud more expensive, or a customer blocked for
nothing?

`class_weight` exists for tree-based models too:

| | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Forest | 0.955 | 0.750 | 0.286 | 0.414 |
| Forest + `balanced` | 0.952 | 0.615 | 0.381 | 0.471 |

The effect is more measured in a forest: recall goes from 0.286 to 0.381 and
precision from 0.75 to 0.615. F1 rises — the most balanced result on this
data.

## Second remedy: moving the threshold

You met the threshold in section 03: `predict` really compares the
`predict_proba` output with 0.5. On imbalanced data 0.5 is almost never the
right place.

```python
probability = model.predict_proba(X_test_scaled)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

The measured sweep:

| Threshold | Precision | Recall | F1 | Caught / 21 |
|---|---|---|---|---|
| 0.50 | 0.750 | 0.286 | 0.414 | 6 |
| 0.30 | 0.500 | 0.286 | 0.364 | 6 |
| 0.20 | 0.500 | 0.333 | 0.400 | 7 |
| **0.10** | 0.342 | 0.619 | **0.441** | 13 |
| 0.05 | 0.262 | 0.762 | 0.390 | 16 |

**F1 peaks at a threshold of 0.10:** 0.441 against 0.414. The same model,
the same coefficients, no retraining — only the place where the decision is
made has moved.

Going down to 0.05 raises recall to 0.762 but drops precision to 0.262 and
F1 comes back down. So "lower the threshold, raise recall" is not an
unlimited strategy.

**Choosing a threshold is a business decision, not a model decision.**
Whoever knows the cost of a false alarm should look at this table and
choose. But the choice must be made **on the training side**, not by looking
at the test set — section 05's rule holds here too.

## Metrics that do not depend on a threshold

Precision, recall and F1 all hang on a single threshold. Is there a way to
measure the model's **ranking ability** — whether it can put the risky
transactions at the top of the list?

```python
from sklearn.metrics import roc_auc_score, average_precision_score

print(roc_auc_score(y_test, probability))           # 0.908
print(average_precision_score(y_test, probability)) # 0.525
```

**ROC AUC is 0.908.** The chance of giving a randomly chosen fraud a higher
probability than a randomly chosen normal transaction is 90.8%. That sounds
excellent.

**Average precision is 0.525.** The same model, the same probabilities. Why
so much lower?

Because **the ROC curve is optimistic on imbalanced data.** It divides the
false positive count by 354 negatives; even 38 false alarms make the rate
only 0.107. The precision-recall curve instead compares false alarms with
**the positives**, and there 38 false alarms look large next to 14 catches.

**The baselines differ too:** a random model's ROC AUC is 0.5, while its
average precision is **the positive rate**, here 0.056. So 0.525 is actually
nine times the baseline — not a bad number, merely not as rosy as 0.908.

| Model | ROC AUC | Average precision |
|---|---|---|
| Logistic regression | 0.908 | 0.525 |
| Random forest | 0.834 | 0.426 |
| Random guessing | 0.500 | 0.056 |

**The rule:** do not report ROC AUC alone on imbalanced data. Average
precision (the area under the PR curve) is far more sensitive to the
minority class.

## Which metric in cross validation

`cross_val_score` computes accuracy by default. On imbalanced data that
comes close to giving the same number in all five folds:

```python
cross_val_score(model, X_train_scaled, y_train, cv=skf, scoring="recall")
```

The measured result:

| `scoring` | Mean | Spread |
|---|---|---|
| `accuracy` | 0.952 | 0.008 |
| `recall` | 0.317 | 0.188 |
| `f1` | 0.397 | 0.183 |
| `roc_auc` | 0.930 | 0.028 |
| `average_precision` | 0.521 | 0.144 |

**Accuracy's spread is 0.008.** Whatever you do, that number does not move;
in a hyperparameter sweep it can never tell you which setting is good.

**Recall's spread is 0.188** — twenty times as much. Each fold holds only
~17 positives, and a few of them escaping moves the number noticeably. That
is **noise**, but at least it carries a real signal too.

`roc_auc` and `average_precision` sit between the two: sensitive to the
minority class yet steadier, since they do not hang on individual records.
Hyperparameter searches on imbalanced data usually use these two.

## Resampling: the thing we did not do

There is a third way to deal with imbalance: **change the data.**

- **Undersampling:** dropping random rows of the majority class. Fast, but
  you are throwing real data away.
- **Oversampling:** duplicating the minority class. It adds no new
  information, repeats the same rows, and the model can memorise them.
- **SMOTE:** generating **synthetic** rows among the minority class's
  neighbours. Not in sklearn; it lives in `imbalanced-learn`.

We used neither here, because:

1. `class_weight` does the same job in most cases **without touching the
   data**.
2. Resampling can only be applied **to the training set**. Sampling the
   validation or test set is another kind of leakage: in the real world the
   fraud rate is 5.7% and the model must see it.
3. Combining it with cross validation takes care — the sampling has to
   happen **inside** each fold, not before. The same leakage trap.

What you need is the names and these three warnings; the library is learned
when it is needed.

## The order of decisions

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>measure the<br>baseline</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>confusion matrix<br>and recall</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>3</b><br>which error<br>is expensive</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>weight and threshold<br>on training</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>5</b><br>report on test:<br>avg precision</span>
  </div>
  <figcaption>The third step is not code but a business decision. Every setting that skips it is arbitrary.</figcaption>
</figure>

## What we left out

- **Multiclass imbalance.** Everything here was for two classes. With three
  or more, separate metrics are computed per class and combined with a
  `macro` or `weighted` average.
- **A cost matrix.** If the monetary cost of a false alarm and of a miss are
  known, the threshold can be chosen by **expected cost** rather than F1.
  The formula is simple; learning the costs is the hard part.
- **Anomaly detection.** When the positive class is as extreme as 0.1%,
  models that look for "deviation from normal" are used instead of
  classification (`IsolationForest`, for example).

This section in one sentence: **on imbalanced data, choosing the metric
matters more than choosing the model.**
