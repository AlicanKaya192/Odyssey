# Monitoring

The model is in production. The server is running, requests return
`200`, no errors. Is the model good? The answers to the first two
questions are in the server logs; the answer to the last one is **not**.
An ML system can quietly get worse while its server runs flawlessly.
**Monitoring** means continuously measuring the health of the model in
production and noticing a decline before the users do. In this section
we watch a model for eight months.

## Three layers

| Layer | What is measured | When it is known |
|---|---|---|
| System | Latency, error rate, number of requests | At once |
| Data and predictions | The distribution of the inputs and of the predictions | At once |
| Model quality | Accuracy, rate of correct predictions | **When the labels arrive** (weeks later) |

The third layer is the most important but arrives last: whether a
customer really cancelled is only known a month later. That is why the
first two layers serve as an **early warning**.

## Eight months

Let's train the model on month 0's data and look at the customers of
every following month. This module's data changes as the months pass:
customers use the service less and pay more.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


TRAIN = make_customers(2000)
model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit([features(r) for r in TRAIN], [r["churned"] for r in TRAIN])

rates, usages, accuracies = [], [], []
print("month  predicted  usage  accuracy")
for month in range(8):
    batch = make_customers(1000, seed=99, month=month)
    X = [features(r) for r in batch]
    rates.append(model.predict(X).mean())
    usages.append(sum(r["usage_hours"] for r in batch) / len(batch))
    accuracies.append(model.score(X, [r["churned"] for r in batch]))
    print(f"{month:>5} {rates[-1]:>10.3f} {usages[-1]:>6.1f} {accuracies[-1]:>9.3f}")
```

```text
month  predicted  usage  accuracy
    0      0.204   32.0     0.813
    1      0.289   30.6     0.820
    2      0.344   29.1     0.778
    3      0.390   27.5     0.784
    4      0.498   25.0     0.673
    5      0.514   23.5     0.681
    6      0.586   22.1     0.685
    7      0.590   21.5     0.658
```

The columns:

- **predicted:** the share of customers the model says "will leave".
  Known at once: every prediction is recorded.
- **usage:** the mean of one of the inputs, the usage hours. Known at
  once.
- **accuracy:** the accuracy. Since the real outcomes only arrive a month
  later, we **can't see** this column when the month ends; we put it
  here for comparison.

The predicted rate climbs steadily from the first month on
(0.204 → 0.590), and usage falls. Accuracy, though, stays
good for three months and drops suddenly in month 4 (0.784 →
0.673). The signals known at once showed the change months
earlier; accuracy only after it broke, and late at that.

`model.predict(X).mean()` gives the share of 1s: the predictions are 0
and 1, so their mean is the rate of those called "will leave".
`f"{month:>5}"` right-aligns, `:>10.3f` gives three digits in a field ten
characters wide.

## The prediction log and delayed labels

To be able to measure quality, every prediction is written into a
**prediction log**: which customer, which month, which model version,
what was predicted. When the real outcome arrives, it is joined with the
log:

```python
import json

log = []
for r in make_customers(5, seed=99, month=4):
    probability = float(model.predict_proba([features(r)])[0, 1])
    log.append({"id": r["id"], "month": 4, "model_version": 3,
                "churn_probability": round(probability, 3)})
print(json.dumps(log[0]))

outcomes = {r["id"]: r["churned"] for r in make_customers(5, seed=99, month=4)}
hits = [(e["churn_probability"] >= 0.5) == bool(outcomes[e["id"]]) for e in log]
print("correct:", sum(hits), "of", len(hits))
```

```text
{"id": "C04-00001", "month": 4, "model_version": 3, "churn_probability": 0.994}
correct: 5 of 5
```

The key of the join is the customer ID. Since the log has the model
version, accuracy can also be computed version by version: is the new
version really better after it went into production? The gate in the
Model Registry section predicted this; the prediction log measures it.

In a real system `outcomes` comes from another table a month later; here
we regenerated it from the same seed. `bool(...)` turns 0 and 1 into
`False` and `True`, so the comparison is made with the same type on both
sides.

## Alerts

There may be nobody looking at a dashboard every day. For monitoring to
work, thresholds and **alerts** are needed. But an alert that goes off at
every small wobble gets ignored after a while; this is called **alert
fatigue**. A simple cure: alert when the threshold is crossed **several
times in a row**.

```python
def alert_months(values, reference, limit, patience=2):
    alerts, streak = [], 0
    for month, value in enumerate(values):
        streak = streak + 1 if abs(value - reference) > limit else 0
        if streak >= patience:
            alerts.append(month)
    return alerts


print("prediction rate alerts:", alert_months(rates, rates[0], 0.1))
print("accuracy alerts:", [m for m, a in enumerate(accuracies) if a < 0.75])
```

```text
prediction rate alerts: [3, 4, 5, 6, 7]
accuracy alerts: [4, 5, 6, 7]
```

The predicted rate alert went off in month 3: the rate
had been more than 0.1 away from the start for two months in a row. The
accuracy alert goes off from month 4 on, but month 4's accuracy can only
be known in month 5. The early signal warned more than a month before.

`streak` counts how many months in a row the threshold was crossed; it
resets when it isn't. `patience` is the number of consecutive months
needed for an alert.

An alert is not a verdict on its own but something **to look at**: the
predicted rate can also rise because the customers really changed (in
this data the churn rate rises too). A person decides what to do:
inspect the data, retrain, or nothing. The next two sections are the
tools for this decision: Data Drift and Concept Drift.

## What to monitor?

Monitoring everything is not possible; a starting list:

- **System:** p95 latency, error rate (the share of `5xx`), number of
  requests.
- **Inputs:** the mean of every numeric column, the missing-value rate,
  the share of requests that break the schema (the share of `422`).
- **Predictions:** the "will leave" rate, the distribution of the
  probabilities.
- **Quality:** accuracy when the labels arrive, and accuracy in slices
  (the slices from the CI for ML section).
- **Version:** how many requests each model version served.

In real systems these measurements are written to a time-series database
such as **Prometheus**, drawn on a dashboard such as **Grafana**, and an
alert is sent when a threshold is crossed.

## Summary

- A healthy server doesn't mean the model is good; an ML system gets
  worse silently.
- Three layers: **system**, **data and predictions** (known at once),
  **model quality** (when the labels arrive, with a delay).
- The lesson's measurement: while the predicted rate had been climbing
  for months, accuracy dropped in month 4; the early signals warned
  beforehand.
- Every prediction is **logged** (ID, version, prediction) and joined
  when the real outcome arrives.
- **Alerts** are built with thresholds; to prevent alert fatigue, several
  crossings in a row are waited for.
- An alert is not a verdict but something to look at.
