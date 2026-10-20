# Experiment Tracking

To find a good model you try dozens of things: another algorithm, another
setting, adding a column, dropping a column. A week later someone asks:
"Which setting gave you 0.83?" The answer is in the corner of a notebook,
in a deleted cell, or nowhere. In this section we write a small
**experiment tracking** tool that records every attempt on its own, and
we learn to choose the right model by looking at the records.

## Three sets

When experimenting, we split the data in three. You remember this from
the Machine Learning path, but here the reason for three matters even
more:

- **Train:** the models are trained on it.
- **Validation:** the experiments are compared on it.
- **Test:** used only at the very end, **once**, for the chosen model.

```python
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(3000))
X_train, X_rest, y_train, y_rest = train_test_split(
    X, y, test_size=0.4, random_state=0)
X_val, X_test, y_val, y_test = train_test_split(
    X_rest, y_rest, test_size=0.5, random_state=0)
print("train:", len(X_train), "validation:", len(X_val), "test:", len(X_test))
```

```text
train: 1800 validation: 600 test: 600
```

First we set 40 percent aside, then split that in two: validation and
test have 600 customers each.

## The log: one file, one line per experiment

Let's keep the record in a file. Every experiment is added to the file
as **one line**; the line is that experiment's JSON. This format is
called **JSON Lines** (the file name often ends in `.jsonl`). It has two
good sides: to add a new experiment, writing one line at the end of the
file is enough and the old lines are never touched; to read it, we open
each line separately with `json.loads`.

```python
import json
from pathlib import Path

LOG = Path("runs.jsonl")


def log_run(params, metrics):
    run_id = len(load_runs()) + 1
    record = {"run": run_id, "params": params, "metrics": metrics}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return run_id


def load_runs():
    if not LOG.exists():
        return []
    lines = LOG.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines]


stays = 1 - sum(y_val) / len(y_val)
log_run({"model": "baseline"}, {"val_accuracy": round(stays, 3)})
print(LOG.read_text(encoding="utf-8"))
```

```text
{"run": 1, "params": {"model": "baseline"}, "metrics": {"val_accuracy": 0.748}}
```

`open("a")` opens the file in **append** mode: the written line goes to
the end of the file and the old ones are not deleted. Every experiment
has a number (`run`), settings (`params`) and measurements (`metrics`).

Our first record isn't even a model: it is the accuracy of saying
"stays" for everyone. This is the **baseline**. Since most customers
stay, even this guess that knows nothing gives 0.748
accuracy. Every model must beat this number first; if the baseline is
not in the record, the question "is 0.80 good?" has no answer.

## Running the experiments

Now let's try two model families with a few settings. Every experiment
goes into the record on its own; no notes by hand:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build(params):
    if params["model"] == "logistic":
        return make_pipeline(StandardScaler(), LogisticRegression(C=params["C"]))
    return RandomForestClassifier(n_estimators=100, max_depth=params["max_depth"],
                                  random_state=0)


experiments = [{"model": "logistic", "C": c} for c in [0.01, 0.1, 1, 10]]
experiments += [{"model": "forest", "max_depth": d} for d in [3, 5, 8, None]]
for params in experiments:
    model = build(params).fit(X_train, y_train)
    log_run(params, {"val_accuracy": round(model.score(X_val, y_val), 3)})
print("runs logged:", len(load_runs()))
```

```text
runs logged: 9
```

`build` builds the model from the settings: the whole recipe of an
experiment is in the `params` dictionary. In logistic regression `C`
sets the strength of regularization; in the forest `max_depth` sets how
many levels deep the trees can grow at most (`None` means no limit).

## Looking at the records

The log file can now be queried like a table. Let's sort the experiments
by validation accuracy:

```python
def val_accuracy(run):
    return run["metrics"]["val_accuracy"]


runs = sorted(load_runs(), key=val_accuracy, reverse=True)
for r in runs:
    settings = ", ".join(f"{k}={v}" for k, v in r["params"].items())
    print(f'{r["run"]:>3}  {r["metrics"]["val_accuracy"]:.3f}  {settings}')
```

```text
3  0.832  model=logistic, C=0.1
  5  0.830  model=logistic, C=10
  2  0.828  model=logistic, C=0.01
  4  0.828  model=logistic, C=1
  7  0.813  model=forest, max_depth=5
  8  0.803  model=forest, max_depth=8
  9  0.788  model=forest, max_depth=None
  6  0.785  model=forest, max_depth=3
  1  0.748  model=baseline
```

What the table tells us:

- Every model beat the baseline; even the worst forest.
- Logistic regression is very close across all four settings. Changing
  `C` adds little here.
- For the forest, depth matters: unlimited depth (`None`) is worse than a
  medium depth. The trees memorize the training data.

`key=val_accuracy` tells the sort which number of each experiment to
look at. `f'{r["run"]:>3}'` right-aligns the number in a field three
characters wide; that is why the columns line up.

## Choose, then test once

Let's choose the best experiment **by validation**, train the model
again and measure it once on the test set. This last measurement goes
into the record too:

```python
best = max(load_runs(), key=val_accuracy)
model = build(best["params"]).fit(X_train, y_train)
test_accuracy = round(model.score(X_test, y_test), 3)
log_run({**best["params"], "final": True},
        {"val_accuracy": best["metrics"]["val_accuracy"], "test_accuracy": test_accuracy})
print("chosen run:", best["run"], best["params"])
print("validation:", best["metrics"]["val_accuracy"], "test:", test_accuracy)
```

```text
chosen run: 3 {'model': 'logistic', 'C': 0.1}
validation: 0.832 test: 0.793
```

The number to report is the **test** result: 0.793. The
0.832 on validation is higher, and that is no accident. Part
of the gap is the luck of the split (in this split the validation set
turned out a little easy), and part of it is **the choice itself**. We
picked the highest of eight experiments on validation; the one that got
lucky is more likely to be picked.

## The winner's curse

Let's measure the effect of choosing on its own. Let's train the same
model, with the same settings, 20 times, changing only its seed. These
20 models are really equally good; every difference between them comes
from luck:

```python
scores = []
for seed in range(20):
    model = RandomForestClassifier(n_estimators=20, random_state=seed)
    model.fit(X_train, y_train)
    scores.append((model.score(X_val, y_val), model.score(X_test, y_test)))
val_mean = sum(v for v, _ in scores) / len(scores)
test_mean = sum(t for _, t in scores) / len(scores)
best_val, its_test = max(scores)
val_lead, test_lead = best_val - val_mean, its_test - test_mean
print(f"validation: best {best_val:.3f}, lead {val_lead:+.3f}")
print(f"test: same run {its_test:.3f}, lead {test_lead:+.3f}")
```

```text
validation: best 0.818, lead +0.028
test: same run 0.757, lead +0.009
```

On validation the best model is +0.028 ahead of the average.
But on test the same model is only +0.009 ahead of the
average: most of the lead we picked vanished on new data. This is called
the **winner's curse**: the best of many candidates looks better on the
data it was measured on than it really is.

This is where experiment tracking pays off too: it shows how many
experiments you ran. The best of three experiments and the best of two
hundred are not the same thing; the more attempts, the more optimistic
the validation result. That is why:

- Choosing is done with **validation**, reporting with **test**.
- The test set is not used for choosing. If you pick every experiment by
  also looking at the test, the test turns into validation and becomes
  optimistic.
- The record keeps **every** attempt, not only the winners; bad results
  are information too.

`max(scores)` compares the tuples by their first element: it gives the
tuple with the highest validation score together with its test score.
`lead` is the chosen model's distance from the average; `:+.3f` writes
the difference with its sign.

## What else goes into the record?

The record in this section keeps only the settings and the
measurements. In a real project the information from the earlier
sections sits next to every experiment too:

- The data fingerprint (Reproducible Training): which data?
- The code version: the Git commit ID.
- The model file's hash (Data and Model Versioning): which model?
- A short note, such as "dropped the fee column": why you tried it.

Tools such as **MLflow** do exactly this: `mlflow.log_param` records a
setting, `mlflow.log_metric` a measurement, and a web interface compares
the experiments in tables and charts. The idea is the same as what we
wrote in this section.

## Summary

- Every experiment must go into the record **on its own**: settings,
  measurements, its number.
- **JSON Lines:** one line per experiment; written in append mode, old
  lines are not touched.
- The record must have a **baseline**; every model must beat it first.
- Experiments are compared on the **validation** set; the chosen model is
  measured once on the **test** set and that is the number reported.
- **The winner's curse:** the best of many candidates looks better than it
  is on the data it was chosen on. The more experiments, the more
  optimistic the validation result.
- Bad results are recorded too.
