# What MLOps Is

In the Machine Learning path you trained a model, measured it on test
data and saw a good number. Most lessons end there. In real work, that
is where the real work begins: the model will meet new data every day,
people will rely on it, the data will change and one day the model will
quietly get worse. This module is about taking a model out of the
notebook and turning it into a **reliable system**. In this section we
see why that is a job of its own and which parts it is made of.

## The module's example: subscription churn

We work with the same example for the whole module. A subscription
service wants to know in advance which customers will cancel their
subscription (**churn**), so that it can offer those customers a
discount. Each customer has five features:

- `tenure`: how many months they have been subscribed
- `monthly_fee`: the monthly fee
- `support_calls`: how many times they called the support line
- `usage_hours`: how many hours a month they use the service
- `plan`: `basic` or `pro`

The target column is `churned`: `1` if the customer cancelled, `0` if
not.

The data does not come from a file but from the `ml_data.py` module,
which sits read-only next to every exercise. `make_customers(n)` produces
the same `n` customers on every computer, because it uses a random
number generator with a fixed seed:

```python
from ml_data import make_customers

rows = make_customers(2000)
print(len(rows), "customers")
for key, value in rows[0].items():
    print(key, "=", value)
churn = sum(r["churned"] for r in rows) / len(rows)
print("churn rate:", round(churn, 3))
```

```text
2000 customers
id = C00-00001
tenure = 67
monthly_fee = 15.78
support_calls = 1
usage_hours = 47.6
plan = basic
churned = 0
churn rate: 0.288
```

About three in every ten customers cancel. `make_customers` also has a
`month` parameter that moves the data forward in time. We will see why
that is needed in a moment.

## Is the model done in the notebook?

Let's train a model as in the Machine Learning path. `plan` is text, so
we turn it into a number (`1` for `pro`):

```python
from sklearn.linear_model import LogisticRegression
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
model = LogisticRegression(max_iter=1000).fit(X, y)

X_test, y_test = to_xy(make_customers(1000, seed=99))
print("test accuracy:", round(model.score(X_test, y_test), 3))
```

```text
test accuracy: 0.813
```

`NUMERIC` holds the names of the four numeric columns in `ml_data.py`.
`seed=99` is a different seed: customers never seen in training. The
model reaches an accuracy of 0.813 on new customers: it gets
roughly four out of five customers right. In the notebook the job looks
done.

Now let's try the same model on the customers who arrive in the months
after it was trained. The model does not change at all; only the
customers do:

```python
for month in [0, 2, 4, 6]:
    X_new, y_new = to_xy(make_customers(1000, seed=99, month=month))
    print("month", month, "accuracy:", round(model.score(X_new, y_new), 3))
```

```text
month 0 accuracy: 0.813
month 2 accuracy: 0.777
month 4 accuracy: 0.674
month 6 accuracy: 0.686
```

In six months the accuracy went from 0.813 to 0.686 and
nobody noticed, because the model raises no error. It keeps producing a
prediction for every customer; the predictions are just wrong far more
often than before. Everything in this module comes down to this sentence: **a
software bug stops the program, but a model getting worse is silent.**

The questions nobody asks in the notebook:

- Which data, which code and which settings was the model trained with?
  Can we reproduce it tomorrow?
- Is a new model really better than the old one? Who decides?
- How does the model reach its users? How many predictions a second can
  it make?
- How will we know the model is getting worse? What do we do then?

## MLOps: machine learning + DevOps

In the CI/CD and DevOps module we built a pipeline for code: on every
change the code was tested, packaged and prepared for release
automatically. **MLOps** (machine learning operations) applies the same
idea to machine learning systems. But there is an important difference:

<figure class="fig">
  <div class="versus">
    <div><h4>Ordinary software</h4>Its behaviour comes from the code alone. As long as the code does not change, the program does the same thing. The pipeline tests and releases the code.</div>
    <div><h4>A machine learning system</h4>Its behaviour comes from the code <b>and the data</b>. Even if the code never changes, the model can get worse when the data changes. The pipeline watches the code, the data and the model together.</div>
  </div>
  <figcaption>An ML system has three things that can change: code, data and model.</figcaption>
</figure>

That is why MLOps has three extra jobs:

1. **Check the data too:** is the data going into training in the
   expected shape? (the Data Validation section)
2. **Version all three together:** which model was produced from which
   data and which code? (Reproducible Training, Versioning, Experiment
   Tracking)
3. **Watch after release:** is the model still good in the real world?
   (Monitoring, Data Drift, Concept Drift)

## The life cycle

The life of an ML system is not a line but a loop:

<figure class="fig">
  <div class="flow">
    <span class="node">Data</span>
    <span class="arrow">→</span>
    <span class="node">Train</span>
    <span class="arrow">→</span>
    <span class="node">Evaluate</span>
    <span class="arrow">→</span>
    <span class="node acc">Serve</span>
    <span class="arrow">→</span>
    <span class="node">Monitor</span>
  </div>
  <figcaption>When monitoring finds a problem, the loop starts again with new data.</figcaption>
</figure>

- **Data:** collect, clean and validate the data.
- **Train:** train the model; record the settings and the result.
- **Evaluate:** compare the new model with the old one on the same
  measure; if it is not good enough, it does not go out.
- **Serve:** make the model usable by whoever needs predictions, for
  example by putting it behind an API.
- **Monitor:** watch the incoming data and how well the predictions do.
  When it gets worse, retrain with new data.

What was missing in the measurement above was the last box: the model
was being served but nobody was monitoring it.

## The model code is the tip of the iceberg

In an ML system, the code that trains the model is usually the smallest
part. Around it is a much larger setup that keeps it working:

<figure class="fig anat">
  <div class="anat-row"><span>Data collection</span><span>Getting the data from its sources regularly.</span></div>
  <div class="anat-row"><span>Data validation</span><span>Catching missing, broken or unexpected values before they reach training.</span></div>
  <div class="anat-row"><span>Feature preparation</span><span>Turning raw data into the numbers the model expects, the same way in training and in serving.</span></div>
  <div class="anat-row"><span><b>Model code</b></span><span>The few lines that train the model.</span></div>
  <div class="anat-row"><span>Registry and versioning</span><span>Keeping track of where every model came from.</span></div>
  <div class="anat-row"><span>Serving</span><span>Giving predictions quickly and reliably.</span></div>
  <div class="anat-row"><span>Monitoring</span><span>Noticing that things are getting worse and raising the alarm.</span></div>
</figure>

When one of these parts is neglected, the system slowly becomes fragile:
nobody can reproduce the model, the data preparation in training and in
serving drift apart, or the decline goes unnoticed for months. In
software this is called **technical debt**: take a shortcut today and you
pay it back with interest tomorrow. In ML systems that debt builds up
outside the code, in the data and in the process.

## Maturity levels

There is a common classification for describing where a team stands
with MLOps:

- **Level 0, manual:** every step is done by hand. Someone trains the
  model in a notebook and hands the file to someone else. Retraining
  takes months.
- **Level 1, an automated training pipeline:** the steps from data to
  model are written as a pipeline; when new data arrives the model is
  retrained and evaluated automatically (continuous training).
- **Level 2, the pipeline itself in CI/CD:** when the training pipeline's
  code changes, it is tested and released too; everything from the
  CI/CD and DevOps module is applied to the training pipeline as well.

Not every team needs level 2. For a small model that changes once a
month, even level 1 may be too much. What matters is knowing which level
the system is at now and choosing according to its risk.

## How we work in this module

- All exercises are Python. The data comes from `ml_data.py`; the
  results are the same on every computer.
- There is no real cloud service, server or account. We see what tools
  such as a model registry, experiment tracking and a feature store do
  by building them ourselves as small Python classes; the lessons also
  name the real tools.
- The models use scikit-learn; what you know from the Machine Learning
  path is enough.

## Summary

- A model that measures well in a notebook is only the start. A model
  can get worse silently: it raises no error and keeps predicting wrong.
- **MLOps** applies the ideas of DevOps to ML systems. The difference:
  behaviour comes from code and data; code, data and model are watched
  together.
- The life cycle: **data → train → evaluate → serve → monitor**, then
  data again.
- The model code is a small part of the system; when validation,
  versioning, serving and monitoring are neglected, technical debt builds
  up.
- Maturity: level 0 manual, level 1 an automated training pipeline, level
  2 the pipeline itself in CI/CD.
