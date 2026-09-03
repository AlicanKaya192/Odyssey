# Classification

So far we have always predicted a **number**: a price. In this section the
target is a **category**: passed or failed, spam or not, ill or healthy.

The flow does not change — read, split, build a baseline, train, measure.
Two things do change: the model used and the **measures**. The second
matters far more than the first.

## There is no such thing as a residual

For regression we computed the error as `actual - predicted`. For
classification that operation is undefined: the difference between "cat" and
"dog" is not a number.

Even with classes coded as `0` and `1`, the distance between them is
invented. With three classes (`0`, `1`, `2`) it is clearer still: the gap
between 2 and 0 is not twice the gap between 1 and 0 — they are simply two
different categories.

So MAE, RMSE and R² are of no use here. A new family of measures is needed.

## Your first classifier

The model is **logistic regression**. Its name says "regression" but the job
it does is classification — a confusing name, for historical reasons.

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
prediction = model.predict(X_test)
```

The three steps are the same. `max_iter` is a hyperparameter: the model
loops while searching for a solution, and the default of 100 rounds is not
enough for some data, which produces a warning.

## Accuracy and the baseline trap

The first measure that comes to mind is **accuracy**: the share of records
you got right.

```python
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, prediction))   # 0.85
```

85%. Is that good?

The same question, the same answer: **look at the baseline.** For
classification the baseline predicts the **most frequent class** for
everything.

```python
most_common = y_train.mode()[0]
baseline = accuracy_score(y_test, [most_common] * len(y_test))
print(baseline)   # 0.675
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Baseline</h4>
      <p>Says "passed" to everyone.<br>Accuracy <b>67.5%</b></p>
    </div>
    <div class="versus-side">
      <h4>Model</h4>
      <p>Decides by looking at three columns.<br>Accuracy <b>85%</b></p>
    </div>
  </div>
  <figcaption>A line that learns nothing is 67.5% correct. The model's 85% only takes on meaning next to it.</figcaption>
</figure>

**The danger here:** unless the two classes are equal in size, the baseline
always lands above 50%. If one class is 95% of the data, a line that learns
nothing is **95% correct**, and the sentence "my model is 94% accurate"
describes a failure.

This is accuracy's biggest problem, and **the whole of section 9 is given
over to it**.

## Opening accuracy up

85% correct — but **which** 85%? Where are the errors?

```python
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, prediction))
# [[ 8  5]
#  [ 1 26]]
```

These four numbers are the **confusion matrix**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">TN = 8</span><span class="anat-body">actual 0, predicted 0 — correctly said "failed" to someone who failed</span></div>
    <div class="anat-row"><span class="anat-label">FP = 5</span><span class="anat-body">actual 0, predicted 1 — <b>said "passed" to someone who failed</b></span></div>
    <div class="anat-row"><span class="anat-label">FN = 1</span><span class="anat-body">actual 1, predicted 0 — <b>said "failed" to someone who passed</b></span></div>
    <div class="anat-row"><span class="anat-label">TP = 26</span><span class="anat-body">actual 1, predicted 1 — correctly said "passed" to someone who passed</span></div>
  </div>
  <figcaption>sklearn returns the matrix in this order: rows are actual, columns predicted. The top-left corner is always TN.</figcaption>
</figure>

Accuracy is computed from these four: `(TN + TP) / total` = `34/40` = 0.85.

**But four numbers say far more than one.** Here there are 5 false positives
against only 1 false negative. The model leans towards saying "passed".

Is that good or bad? It depends:

- For a **scholarship** decision, giving one to someone who does not deserve
  it (FP) is expensive.
- For a **support class** decision, missing someone who needs it (FN) is
  expensive.

The same model, the same numbers — a different conclusion.

## Precision and recall

The confusion matrix has four numbers; we reduce them to two meaningful
ratios.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Precision</h4>
      <p><code>TP / (TP + FP)</code></p>
      <p>"Of those I called passed, how many really did?"<br><b>26/31 = 0.839</b></p>
    </div>
    <div class="versus-side">
      <h4>Recall</h4>
      <p><code>TP / (TP + FN)</code></p>
      <p>"Of those who passed, how many did I find?"<br><b>26/27 = 0.963</b></p>
    </div>
  </div>
  <figcaption>Precision measures how clean your predictions are, recall how wide your net is.</figcaption>
</figure>

The way to keep them apart is to **look at the denominator**:

- Precision's denominator is **your predictions** — how trustworthy you were
  when you spoke.
- Recall's denominator is **what actually exists** — how many of them you
  caught.

**Which one matters depends on the problem:**

| Problem | Priority | Why |
|---|---|---|
| Disease screening | **Recall** | Missing a patient costs more than an extra test |
| Spam filter | **Precision** | Sending a real email to spam is worse than letting one spam through |
| Fraud detection | **Recall** | A missed transaction is money lost |
| Recommendations | **Precision** | A bad recommendation loses the user |

## F1: reducing the two to one

When one number is wanted instead of two, **F1** is used:

```
F1 = 2 x (precision x recall) / (precision + recall)
```

This is a **harmonic mean**, and how it differs from an ordinary average
matters: if either is very low, F1 is low too.

Think of a model with precision 1.0 and recall 0.02 — it calls exactly one
person ill and gets it right. An ordinary average would give 0.51 and look
acceptable. F1 gives **0.039**.

**F1 is a convenience, not a solution.** Seeing precision and recall
separately is always more informative; F1 earns its place only when you need
to rank models.

## The threshold: the model's hidden setting

`predict` gives you a `0` or a `1`. But inside the model there is a
**probability**:

```python
probability = model.predict_proba(X_test)[:, 1]
```

`predict` says 1 when that probability is **above 0.5**. The 0.5 is not the
result of a calculation but a **default** — and it can be changed.

```python
prediction = (probability >= 0.3).astype(int)
```

Here is what moving the threshold does:

```
threshold   precision   recall
   0.30       0.818      1.000
   0.50       0.839      0.963
   0.70       0.889      0.889
```

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Threshold ↓</b><br>says "1" more often</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Recall ↑</b><br>misses fewer</span>
    <span class="arrow">+</span>
    <span class="node acc"><b>Precision ↓</b><br>more false alarms</span>
  </div>
  <figcaption>Lowering the threshold is a trade: fewer misses, more false alarms. There is no free improvement.</figcaption>
</figure>

Drop the threshold to 0.30 and recall is **1.000** — not a single passing
student is missed. The price is a drop in precision.

**This is an adjustment made without retraining.** The same model, the same
coefficients; only the point where the decision is made moves. For a disease
screening, lowering the threshold is usually right; for a spam filter,
raising it is.

## All of it in one call

```python
from sklearn.metrics import classification_report
print(classification_report(y_test, prediction))
```

```
              precision    recall  f1-score   support

           0       0.89      0.62      0.73        13
           1       0.84      0.96      0.90        27

    accuracy                           0.85        40
```

**There is a separate row per class**, and that matters: the model's recall
is 0.96 on class `1` but 0.62 on class `0`. It is far worse at finding the
students who fail — and a single accuracy figure hid that completely.

`support` says how many records each class has: 13 against 27. That is where
you read the imbalance.

## What we skipped in this section

- **The ROC curve and AUC.** A measure that evaluates every threshold at
  once. It reduces the threshold trade-off to a single number; it arrives in
  the imbalanced-data section.
- **Multiclass problems.** Everything here was for two classes. With three
  or more, precision and recall are computed per class and then averaged —
  that is where `macro` and `weighted` averages come from.
- **Serious imbalance.** When one class is 95% of the data, even the
  measures in this section can mislead. That is section 9.

For now you have two things: you can build a model when the target is a
category, and you know not to trust a single accuracy figure. The second is
worth more.
