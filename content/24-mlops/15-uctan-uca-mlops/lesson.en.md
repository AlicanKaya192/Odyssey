# Capstone: An End-to-End MLOps Pipeline

Every section of this module built one part. In the capstone we join the
parts into a single pipeline: one that runs by itself every month,
monitors the model, retrains it when needed, and checks both the data and
the new model. Then we run the pipeline for eight months and read what it
decided each month.

## The pipeline's map

<figure class="fig">
  <div class="flow">
    <span class="node">Monitor</span>
    <span class="arrow">→</span>
    <span class="node">Trigger</span>
    <span class="arrow">→</span>
    <span class="node">Validate</span>
    <span class="arrow">→</span>
    <span class="node">Train</span>
    <span class="arrow">→</span>
    <span class="node acc">Gate</span>
  </div>
  <figcaption>The model that passes the gate is released and monitored; the loop turns every month.</figcaption>
</figure>

| Step | What it does | Section |
|---|---|---|
| Monitor | Drift in today's inputs, accuracy with last month's labels | Monitoring, Data Drift |
| Trigger | Starts retraining if accuracy dropped or the drift is large | Concept Drift |
| Validate | Looks at the share of invalid rows in the training window | Data Validation |
| Train | Trains on the last two months with a fixed seed | Reproducible Training |
| Gate | Compares the new model with the live one on a current set | Model Registry, CI for ML |

## The pieces

Let's bring together shortened versions of the earlier sections' pieces:
the validation rules, training, accuracy and PSI. The pipeline's state
(the live model, the data it was trained on, its version and its gate
score) lives in a dictionary:

```python
import bisect
import math
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC

LIMITS = {"tenure": (1, 72), "monthly_fee": (5, 100),
          "support_calls": (0, 10), "usage_hours": (0, 100)}


def valid(row):
    if row["plan"] not in ("basic", "pro"):
        return False
    return all(low <= row[c] <= high for c, (low, high) in LIMITS.items())


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


def train(rows):
    model = make_pipeline(StandardScaler(), LogisticRegression())
    return model.fit([features(r) for r in rows], [r["churned"] for r in rows])


def accuracy(model, rows):
    score = model.score([features(r) for r in rows], [r["churned"] for r in rows])
    return round(score, 3)


def psi(reference, current, bins=10):
    ordered = sorted(reference)
    edges = [ordered[len(ordered) * i // bins] for i in range(1, bins)]

    def shares(values):
        counts = [0] * bins
        for v in values:
            counts[bisect.bisect_left(edges, v)] += 1
        return [max(c / len(values), 0.0001) for c in counts]

    ref, cur = shares(reference), shares(current)
    return sum((c - r) * math.log(c / r) for r, c in zip(ref, cur))


def column(rows, name):
    return [r[name] for r in rows]


def drift(reference, current):
    values = [psi(column(reference, n), column(current, n)) for n in NUMERIC]
    return round(max(values), 3)


first = make_customers(2000)
model = train(first)
state = {"model": model, "reference": first, "version": 1,
         "base": accuracy(model, make_customers(1000, seed=99))}
print("v1 accuracy:", state["base"])
```

```text
v1 accuracy: 0.813
```

`drift` computes the PSI of every numeric column and gives the largest: one
column drifting is enough for the trigger. `base` is the score the live
model got when passing the gate; in monitoring, accuracy is compared with
it.

## The monthly step

The work the pipeline does every month is a single function. The
thresholds are at the top, with names; these are the numbers in the design
document:

```python
MAX_DROP, MAX_DRIFT, MAX_INVALID, MIN_GAIN = 0.05, 0.25, 0.05, 0.003
BROKEN = {5}


def run_month(month, state):
    today = make_customers(1000, seed=5, month=month)
    holdout = make_customers(1000, seed=99, month=month - 1)
    moved = drift(state["reference"], today)
    live = accuracy(state["model"], holdout)
    report = f"month {month}: drift {moved:.3f} acc {live:.3f} ->"
    if live >= state["base"] - MAX_DROP and moved <= MAX_DRIFT:
        return f"{report} keep"
    older = make_customers(500, seed=7, month=max(month - 2, 0))
    window = older + make_customers(500, seed=7, month=month - 1)
    if month in BROKEN:
        for row in window:
            row["monthly_fee"] = round(row["monthly_fee"] * 100)
    invalid = sum(not valid(r) for r in window) / len(window)
    if invalid > MAX_INVALID:
        return f"{report} data rejected ({invalid:.0%} invalid)"
    candidate = train(window)
    score = accuracy(candidate, holdout)
    if score < live + MIN_GAIN:
        return f"{report} candidate kept out ({score:.3f})"
    state.update(model=candidate, reference=window, base=score)
    state["version"] += 1
    return f"{report} v{state['version']} promoted ({score:.3f})"
```

The steps follow the map:

- **Monitor:** `today` is this month's inputs (no labels), `holdout` is
  last month's customers whose labels have arrived. Drift looks at today,
  accuracy at last month; this is the label delay.
- **Trigger:** if accuracy didn't drop by `MAX_DROP` from `base` and the
  drift didn't exceed `MAX_DRIFT`, nothing is done.
- **Validate:** the training window is the last two months (Concept
  Drift). `BROKEN` **imitates** the data source switching the fees to
  cents in month 5 (the error from the Data Validation section).
- **Train** and **Gate:** the candidate is measured **on the same current
  set** as the live model and stays out unless it is better by at least
  `MIN_GAIN`.

## Eight months

```python
for month in range(1, 8):
    print(run_month(month, state))
print("live model: v" + str(state["version"]))
```

```text
month 1: drift 0.070 acc 0.813 -> keep
month 2: drift 0.185 acc 0.820 -> keep
month 3: drift 0.578 acc 0.778 -> v2 promoted (0.782)
month 4: drift 0.326 acc 0.787 -> candidate kept out (0.784)
month 5: drift 0.575 acc 0.691 -> data rejected (100% invalid)
month 6: drift 0.922 acc 0.697 -> v3 promoted (0.837)
month 7: drift 0.127 acc 0.821 -> keep
live model: v3
```

Every line tells of a decision:

| Month | What happened | Why |
|---|---|---|
| 1–2 | The model stayed | Small drift, accuracy in place |
| 3 | v2 passed | Drift 0.578; the candidate slightly better than the live model |
| 4 | The candidate stayed out | The drift was large again, but the candidate wasn't better than the live model |
| 5 | The data was rejected | Accuracy fell to 0.691, but the whole window was invalid |
| 6 | v3 passed | The candidate trained on clean data: 0.837 |
| 7 | The model stayed | Small drift against the new reference |

Three things are worth noticing. In month 4 the drift threshold triggered
retraining, but the **gate** stopped a pointless model change: drift alone
doesn't change the model. In month 5 the pipeline **couldn't** change the
model exactly when it needed to most. What would have happened without
validation? The candidate trained on the broken data would score
0.784 on a set from the same broken source and pass the
gate; the day the source was fixed, it would drop to
0.673 accuracy on clean data. The gate alone isn't
enough: the gate's set can come from the same broken source too. The price
of the rejection is customers facing the old model for one more month;
that's why validation should also send an **alert**, and someone should
fix the data source. In month 6 the model recovered with clean data.

## Running it every month

Once the pipeline is a script (`pipeline.py`), running it every month is a
workflow. The tests run first; the pipeline's report is kept whatever the
result:

```yaml
name: Monthly model

on:
  schedule:
    - cron: "0 3 1 * *"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q

  retrain:
    needs: test
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python pipeline.py
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: pipeline-report
          path: report.txt
```

`"0 3 1 * *"` means 03:00 (UTC) on the 1st of every month.
`workflow_dispatch` lets the pipeline be started by hand too: when the
quality alert goes off, without waiting for the schedule ("both" from
Concept Drift).

## The module's map

| Section | Its place in the pipeline |
|---|---|
| Reproducible Training | `train`: the same data, the same model |
| Data Validation | `valid` and `MAX_INVALID` |
| Data and Model Versioning, Experiment Tracking | In a real pipeline the window's digest and the candidate's measurements are recorded (shortened here) |
| Model Registry | `state`: the version, the live model, the gate score |
| CI for ML | The tests and the gate in the workflow |
| Serving a Model, Scaling | Nightly batch scoring with the live model |
| Training-Serving Skew | The same `features` in both training and serving |
| Monitoring, Data Drift | `drift` and the `holdout` accuracy |
| Concept Drift | The last window, a current gate set |
| A/B Tests, Shadow and Canary | Releasing the model that passed step by step |
| ML System Design | The thresholds and the fallback |

## Summary

- Every month the pipeline turns in this order: monitor, trigger,
  validate, train, pass the gate.
- The thresholds (`MAX_DROP`, `MAX_DRIFT`, `MAX_INVALID`, `MIN_GAIN`) are
  written with names; they are the decisions in the design document.
- The lesson's eight months: v2 in month 3, the candidate kept out in
  month 4, broken data rejected in month 5, v3 in month 6.
- Drift alone doesn't change the model; the gate decides.
- Validation stops broken data but leaves the model old; a rejection
  should also send an alert. The gate alone isn't enough: its set can be
  broken too.
- A workflow runs the pipeline every month and by hand; the report is kept
  in every case.
