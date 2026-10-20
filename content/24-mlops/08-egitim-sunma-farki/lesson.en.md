# Training-Serving Skew and the Feature Store

The model gave 0.81 accuracy on the test, passed the gate and went into
production. A week later the customer team asks: "Most of the customers
we called were going to stay anyway; why?" The model is the same model;
what changed is the input it is given. If the features are computed one
way in training and another way in production, the model sees a different
world in production. This is called **training-serving skew**. In this
section we measure two forms of it and look at its cure, the **feature
store**.

## The features in training

The model is trained seeing the features in this order: tenure, fee,
support calls, usage, plan.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers

NAMES = ["tenure", "monthly_fee", "support_calls", "usage_hours", "is_pro"]


def features(r):
    return [r["tenure"], r["monthly_fee"], r["support_calls"], r["usage_hours"],
            1 if r["plan"] == "pro" else 0]


TRAIN = make_customers(2000)
HOLD = make_customers(1000, seed=99)
y_train = [r["churned"] for r in TRAIN]
y_hold = [r["churned"] for r in HOLD]


def accuracy(model, make, rows):
    return round(model.score([make(r) for r in rows], y_hold), 3)


X_train = [features(r) for r in TRAIN]
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
print("offline accuracy:", accuracy(model, features, HOLD))
```

```text
offline accuracy: 0.813
```

## The same feature, two pieces of code

Another team writes the service that serves the model. Instead of copying
the feature code they rewrite it, and mix up the places of two columns:
the fee and the support calls swap.

```python
def serve_features(r):
    return [r["tenure"], r["support_calls"], r["monthly_fee"], r["usage_hours"],
            1 if r["plan"] == "pro" else 0]


print("served accuracy:", accuracy(model, serve_features, HOLD))
```

```text
served accuracy: 0.297
```

The accuracy fell from 0.813 to 0.297: worse
even than saying "stays" for everyone (0.703). No error was
raised: both columns are numbers, the model took the numbers and
computed. The model now reads a fee of 30 as "called support 30 times";
it thinks almost everyone will leave.

## Catching the skew

The way to catch this mistake is to **record the features that go into
the model at serving time** and compare them with the ones in training.
It is the same idea as the profile in the Data Validation section, but
this time the source is not the raw data but the vector that goes into
the model:

```python
def column_means(rows):
    return [sum(column) / len(column) for column in zip(*rows)]


served = [serve_features(r) for r in HOLD]
pairs = zip(NAMES, column_means(X_train), column_means(served))
for name, trained, live in pairs:
    flag = "CHECK" if abs(live - trained) > 0.5 * abs(trained) else "ok"
    print(f"{name:14} {trained:7.2f} {live:7.2f}  {flag}")
```

```text
tenure           36.68   37.67  ok
monthly_fee      30.23    0.73  CHECK
support_calls     0.74   29.80  CHECK
usage_hours      32.18   32.00  ok
is_pro            0.41    0.40  ok
```

Two columns stand out at once: the mean of the fee went from 30 to 0.7,
and that of the support calls from 0.7 to 30. `zip(*rows)` turns a list
of rows into columns: the first element is the first value of every row,
the second the second values. If the inputs at serving time are not
recorded, this comparison can't be made; that is why recording them is a
must.

The real cure, though, is for the skew never to appear: the feature code
is written **in one place**, and both training and serving import the
same function (`from features import features`). Feature code that is
copied or rewritten drifts apart sooner or later.

## A feature that sees the future

The second kind of skew is sneakier. The training data holds the
customer's **total** support calls; but customers who cancel also call a
few times while cancelling. At prediction time these calls **don't exist
yet**: the model asks "will this customer leave?" before the
cancellation. Let's measure this information leaking into the training
data:

```python
import random


def with_exit_calls(rows, seed):
    rng = random.Random(seed)
    result = []
    for r in rows:
        exit_calls = rng.randint(1, 3) if r["churned"] else 0
        result.append({**r, "calls_total": r["support_calls"] + exit_calls})
    return result


def leaky_features(r):
    return [r["tenure"], r["monthly_fee"], r["calls_total"], r["usage_hours"],
            1 if r["plan"] == "pro" else 0]


X_leaky = [leaky_features(r) for r in with_exit_calls(TRAIN, 1)]
leaky = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_leaky, y_train)
test_rows = with_exit_calls(HOLD, 2)
print("leaky, offline:", accuracy(leaky, leaky_features, test_rows))
live_rows = [{**r, "calls_total": r["support_calls"]} for r in HOLD]
print("leaky, live:", accuracy(leaky, leaky_features, live_rows))
```

```text
leaky, offline: 0.939
leaky, live: 0.787
```

On the test, 0.939: it looks great. But the test set was
prepared with the same mistake; it contains the cancellation calls too.
In production these calls haven't happened yet, so the accuracy falls to
0.787: **worse** than the 0.813 of the model
without the leak. The model overdid the rule "whoever calls a lot
leaves"; in production, when those calls don't come, it gets it wrong.

This is called **point-in-time leakage**: information that couldn't be
known at prediction time was used in training. Building the test with the
same mistake makes it invisible; it only shows up in production.

## What was known at the time?

The cure is to compute every feature **as of the prediction time**: take
the last value known on that date. For this, feature values are stored
with their dates and the query is made "as of" a date:

```python
calls_history = [["2026-01-01", 0], ["2026-02-01", 1], ["2026-03-01", 4]]


def as_of(history, day):
    value = None
    for when, known in history:
        if when <= day:
            value = known
        else:
            break
    return value


print("as of 2026-02-15:", as_of(calls_history, "2026-02-15"))
print("as of 2026-03-10:", as_of(calls_history, "2026-03-10"))
print("as of 2025-12-31:", as_of(calls_history, "2025-12-31"))
```

```text
as of 2026-02-15: 1
as of 2026-03-10: 4
as of 2025-12-31: None
```

If the customer cancelled on 15 February, "1 call" is used for them in
training, not March's 4. Comparisons like `"2026-02-15" <= "2026-03-01"`
are text comparisons but work correctly: when a date is written as
`YYYY-MM-DD`, alphabetical order is the same as time order. The list is
sorted by date, so we stop at the first later date (`break`).

## The feature store

The common cure for both problems is a **feature store**:

- Features are defined **once**; training and serving use the same
  definition. The column order can't get mixed up.
- The **offline store** keeps the dated history of every feature. Training
  data is pulled "as of the label date"; there is no point-in-time
  leakage.
- The **online store** keeps every customer's **latest** values; at
  serving time they are read by customer ID within milliseconds.

A small example:

```python
class FeatureStore:
    def __init__(self):
        self.history = {}

    def write(self, customer, day, values):
        self.history.setdefault(customer, []).append([day, values])

    def offline(self, customer, day):
        return as_of(self.history[customer], day)

    def online(self, customer):
        return self.history[customer][-1][1]


store = FeatureStore()
store.write("C7", "2026-01-01", {"support_calls": 0, "usage_hours": 35.0})
store.write("C7", "2026-02-01", {"support_calls": 1, "usage_hours": 28.0})
store.write("C7", "2026-03-01", {"support_calls": 4, "usage_hours": 9.0})
print("for training, as of 2026-02-15:", store.offline("C7", "2026-02-15"))
print("for serving, now:", store.online("C7"))
```

```text
for training, as of 2026-02-15: {'support_calls': 1, 'usage_hours': 28.0}
for serving, now: {'support_calls': 4, 'usage_hours': 9.0}
```

For training the question is "what was known on 15 February?", for
serving "what is known now?". Both read from the same writes; the
definition is one.

In real projects, open-source feature stores such as **Feast** provide
these two stores, definition files and the "as of" join ready-made.

## Summary

- **Training-serving skew:** in production the model sees inputs computed
  differently from training. No error is raised; only the predictions
  break.
- The lesson's measurement: two columns swapping places brought the
  accuracy down from 0.813 to 0.297.
- The features that go into the model at serving time are **recorded**
  and compared with those in training.
- The feature code is written **in one place**; training and serving
  import it.
- **Point-in-time leakage:** using in training information that couldn't
  be known at prediction time. If the test is built with the same mistake,
  it only shows up in production.
- Every feature is computed **as of** the prediction time.
- **Feature store:** one definition, a dated offline store (training) and
  an online store with the latest values (serving).
