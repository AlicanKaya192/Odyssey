# Concept Drift and Retraining

In the Data Drift section we saw the model stay good for three months
although the inputs drifted. Then in month 4 the accuracy dropped
suddenly. What changed that month was not the customers but **how they
decide**: the price now matters much more, and support calls not as much
as before. A change in the relationship between input and outcome is
called **concept drift**. In this section we measure how to notice it and
**how to retrain** the model.

## Two drifts

| | Data drift | Concept drift |
|---|---|---|
| What changes | The distribution of the inputs | The relationship between input and outcome |
| Example | Customers pay more | The same fee now leads to more cancellations |
| Visible without labels | Yes | No, labels are needed |
| Effect on the model | Sometimes harmless | The model now knows the wrong rule |

The shared pieces: features, training and monthly accuracy.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC

NAMES = NUMERIC + ["is_pro"]


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


def fit(rows):
    model = make_pipeline(StandardScaler(), LogisticRegression())
    return model.fit([features(r) for r in rows], [r["churned"] for r in rows])


def accuracy(model, month):
    rows = make_customers(1000, seed=99, month=month)
    X = [features(r) for r in rows]
    return round(model.score(X, [r["churned"] for r in rows]), 3)


first = fit(make_customers(2000))
print("month 0:", accuracy(first, 0), " month 4:", accuracy(first, 4))
```

```text
month 0: 0.813  month 4: 0.673
```

## Seeing concept drift

The simplest test once labels arrive: compare the average churn
probability the model **gives** with the churn rate that **happened**. If
the model knows the world correctly, the two are close:

```python
print("month  predicted  actual")
for month in range(8):
    rows = make_customers(1000, seed=99, month=month)
    predicted = first.predict_proba([features(r) for r in rows])[:, 1].mean()
    actual = sum(r["churned"] for r in rows) / len(rows)
    print(f"{month:>5} {predicted:>10.3f} {actual:>7.3f}")
```

```text
month  predicted  actual
    0      0.277   0.297
    1      0.346   0.347
    2      0.385   0.358
    3      0.425   0.410
    4      0.504   0.413
    5      0.526   0.469
    6      0.576   0.471
    7      0.573   0.488
```

For the first four months the two columns are close: the model gives the
right probabilities even though the inputs drift. From month 4 on the
model keeps expecting **too much** churn (0.504 expected,
0.413 happened). A model's probabilities agreeing with reality is
called **calibration**; calibration breaking suddenly is a sign of concept
drift.

`predict_proba(...)[:, 1].mean()` is the average churn probability per
customer, not the mean of 0/1 predictions as with `predict(...).mean()`.

## What changed?

Logistic regression gives each feature a weight; comparing the weights
shows how the relationship changed. Let's compare the first model with a
model trained on the customers of months 4 and 5:

```python
window = make_customers(500, seed=7, month=4) + make_customers(500, seed=7, month=5)
recent = fit(window)
old_w = first.named_steps["logisticregression"].coef_[0]
new_w = recent.named_steps["logisticregression"].coef_[0]
for name, a, b in zip(NAMES, old_w, new_w):
    print(f"{name:14} {a:6.2f} {b:6.2f}")
```

```text
tenure          -1.25  -1.31
monthly_fee      0.87   1.89
support_calls    1.02   0.24
usage_hours     -0.70  -0.62
is_pro          -0.38  -0.07
```

The fee's weight more than doubled, and the support calls' weight fell
below a quarter. The old model knows "whoever calls a lot leaves"; in the
new world the real reason is the price. Since the features are scaled
(`StandardScaler`), the weights can be compared with each other.
`named_steps` reaches the steps inside the pipeline by name.

## Which data to retrain with?

We are at the end of month 5; the labels of months 4 and 5 have arrived.
There are three choices:

- **Don't retrain:** carry on with the first model.
- **The whole history:** train with all of months 0–5.
- **The last window:** train only with the last two months (4–5).

Let's measure which is good by looking at **the future**: months 6 and 7,
customers no model has seen.

```python
history = []
for month in range(6):
    history += make_customers(500, seed=7, month=month)
choices = {"never": first, "all history": fit(history), "last window": recent}
for name, model in choices.items():
    print(f"{name:12} month 6: {accuracy(model, 6)}  month 7: {accuracy(model, 7)}")
```

```text
never        month 6: 0.685  month 7: 0.658
all history  month 6: 0.759  month 7: 0.742
last window  month 6: 0.821  month 7: 0.798
```

The last window won by far. Training with the whole history **mixes** the
old relationship (calls matter) with the new one (the price matters):
there is plenty of data, but half of it describes a world that is now
wrong. If the concept has drifted, old data doesn't help; it does harm.

But it isn't always like this: if the concept hasn't drifted, more data
means a better model, and since the last window is small it is open to
luck. The window's size is a **choice**; the right way is to decide by
measuring a few sizes on a later period, as in the Experiment Tracking
section.

## The gate trap

The new model must pass the gate (Model Registry). But on **which**
evaluation set? The old evaluation set in the registry is from month 0:

```python
for name, model in [("first", first), ("last window", recent)]:
    old_set, new_set = accuracy(model, 0), accuracy(model, 5)
    print(f"{name:12} on month 0: {old_set}  on month 5: {new_set}")
```

```text
first        on month 0: 0.813  on month 5: 0.681
last window  on month 0: 0.718  on month 5: 0.837
```

On the old set (month 0) the old model looks better: the gate would
**turn the new model away**. On the current set (month 5) the new model is
better by far. When the concept drifts, the evaluation set goes stale
too; the gate must work with a **current, labelled** set. Otherwise the
pipeline rejects the model that adapted to the world and keeps the old
one.

## When to retrain?

| Way | How | Plus | Minus |
|---|---|---|---|
| On a schedule | Every month, every week | Simple, predictable | Runs even when not needed; late for a sudden change |
| On a trigger | When the quality alert goes off | Runs when needed | As late as the label delay |
| Both | Schedule + an emergency trigger | A common choice | More parts |

Retraining is not just producing a new model; it goes through the whole
pipeline: pull the data as of a date (Training-Serving Skew), validate it
(Data Validation), train and record it (Reproducible Training, Experiment
Tracking), pass the gate on a **current** set, put it in the registry
(Model Registry), release it and monitor it. Every section in this module
is a link of this loop.

## Summary

- **Concept drift:** the relationship between input and outcome changing.
  It can't be seen without labels.
- Its sign: the average probability the model gives and the rate that
  happened diverging (**calibration** breaks).
- The lesson's measurement: the fee's weight more than doubled, and the
  support calls' fell below a quarter.
- If the concept drifted, training with the **last window** can beat the
  whole history: old data teaches the wrong relationship.
- The window size is a choice; it is chosen by measuring on a later period.
- The gate must work with a **current** labelled set; an old set unfairly
  rejects the new model.
- Retraining is done on a schedule, on a trigger, or both, and goes
  through the whole pipeline.
