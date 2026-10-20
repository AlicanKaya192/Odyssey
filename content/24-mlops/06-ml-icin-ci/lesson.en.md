# CI for ML: The Quality Gate

In the CI/CD and DevOps module we built a pipeline that runs the tests
on every change. In an ML project that pipeline is not enough: the model
can get worse while all the tests pass. Someone changing a setting by
mistake doesn't break the code but does break the model. In this section
we add a step to the pipeline that tests **the model too**: a **quality
gate**. If the model doesn't clear the bar, the pipeline turns red and
the change is not merged.

## What is tested in an ML pipeline?

| What | Example test | Which section |
|---|---|---|
| Code | Does the feature function give the right columns in the right order? | This section |
| Data | Does it fit the schema, has the profile shifted? | Data Validation |
| Reproducibility | Do two trainings with the same settings give the same predictions? | Reproducible Training |
| Model | Does the accuracy clear the bar, in every customer group? | This section |
| Behavior | Does the model react in the expected direction? | This section |

First let's build the shared pieces: the feature function, the training
data, the evaluation set and the baseline.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(row):
    return [row[c] for c in NUMERIC] + [1 if row["plan"] == "pro" else 0]


TRAIN = make_customers(2000)
HOLD = make_customers(1000, seed=99)
BASELINE = 1 - sum(r["churned"] for r in HOLD) / len(HOLD)


def train(model):
    return model.fit([features(r) for r in TRAIN], [r["churned"] for r in TRAIN])


print("baseline:", round(BASELINE, 3))
```

```text
baseline: 0.703
```

## Testing the code

The code that prepares the model's input is an ordinary function; it is
tested with ordinary unit tests. If the order of the columns changes,
the model doesn't raise an error but sees the wrong columns in the wrong
places, so we test the order too:

```python
def test_feature_order():
    row = {"tenure": 5, "monthly_fee": 20.0, "support_calls": 1,
           "usage_hours": 30.0, "plan": "pro"}
    assert features(row) == [5, 20.0, 1, 30.0, 1]


def test_basic_plan_is_zero():
    row = {"tenure": 5, "monthly_fee": 20.0, "support_calls": 1,
           "usage_hours": 30.0, "plan": "basic"}
    assert features(row)[-1] == 0


for test in [test_feature_order, test_basic_plan_is_zero]:
    test()
    print(test.__name__, "passed")
```

```text
test_feature_order passed
test_basic_plan_is_zero passed
```

In a real project these functions live in a `test_features.py` file and
`pytest` finds and runs them itself (the Automated Tests section of the
CI/CD and DevOps module). `test.__name__` gives the function's name.

## The quality gate

Now the model itself. The gate's rules ask three questions:

- **Is it good enough?** Is the accuracy above a floor?
- **Does it clearly beat the baseline?** Is it better than saying
  "stays" for everyone by at least a certain margin?
- **Is it good in every group?** The model can be very bad in one group
  of customers while the average looks good. Let's look at the plans
  (`basic`, `pro`) separately. A certain part of the data is called a
  **slice**.

```python
RULES = {"min_accuracy": 0.78, "min_lift": 0.05, "min_slice": 0.75}


def accuracy_on(model, rows):
    X = [features(r) for r in rows]
    return model.score(X, [r["churned"] for r in rows])


def quality_gate(model):
    failures = []
    accuracy = accuracy_on(model, HOLD)
    if accuracy < RULES["min_accuracy"]:
        failures.append(f"accuracy {accuracy:.3f} is below the floor")
    if accuracy < BASELINE + RULES["min_lift"]:
        failures.append(f"accuracy {accuracy:.3f} is too close to the baseline")
    for plan in ["basic", "pro"]:
        part = accuracy_on(model, [r for r in HOLD if r["plan"] == plan])
        if part < RULES["min_slice"]:
            failures.append(f"{plan} slice: {part:.3f} is too low")
    return failures


good = train(make_pipeline(StandardScaler(), LogisticRegression()))
print("good model:", quality_gate(good))
weak = train(make_pipeline(StandardScaler(), LogisticRegression(C=0.0001)))
print("weak model:")
for failure in quality_gate(weak):
    print(" ", failure)
```

```text
good model: []
weak model:
  accuracy 0.703 is below the floor
  accuracy 0.703 is too close to the baseline
  basic slice: 0.735 is too low
  pro slice: 0.654 is too low
```

The good model passed the gate: the list of problems is empty. In the
second model someone made `C` very small: the regularization is so strong
that the model can learn almost nothing. The code raised no error and
all the unit tests still pass; but the gate caught four problems at
once. Its accuracy is the same as the baseline (0.703): the
model does nothing better than saying "stays" for everyone. Both plans are below
the slice bar; the drop for `pro` customers is even bigger than in the
average.

In the pipeline this gate runs as a separate script (`check_quality.py`)
and at the very end says `sys.exit(1 if failures else 0)`: if there is a
problem, the script ends with an error code and the step turns red.

## Behavioral tests

Accuracy says **how often** the model is right; it doesn't say **how** it
thinks. **Behavioral tests** look at whether the model reacts sensibly.
In this module's data, churn grows as support calls grow. So when a
customer's support calls go up by two, the churn probability the model
gives should **not go down**. This is called a **directional test**:

```python
def directional_share(model, rows):
    before = model.predict_proba([features(r) for r in rows])[:, 1]
    more_calls = [{**r, "support_calls": r["support_calls"] + 2} for r in rows]
    after = model.predict_proba([features(r) for r in more_calls])[:, 1]
    return float((after >= before).mean())


forest = train(RandomForestClassifier(n_estimators=100, random_state=0))
print("logistic:", round(directional_share(good, HOLD), 3))
print("forest:", round(directional_share(forest, HOLD), 3))
obvious = {"tenure": 2, "monthly_fee": 45.0, "support_calls": 6,
           "usage_hours": 5.0, "plan": "pro"}
probability = good.predict_proba([features(obvious)])[0, 1]
print("obvious churner:", round(float(probability), 3))
```

```text
logistic: 1.0
forest: 0.957
obvious churner: 1.0
```

`predict_proba(...)[:, 1]` gives every customer's probability of
churning (class 1). `(after >= before).mean()` is the share of customers
for whom the condition holds: `True` counts as 1, `False` as 0.

In logistic regression the directional test held for every customer: the
model gives each column a single weight, and if the weight is positive
the direction is always the same. In the forest it held for
95.7% of the customers: trees split numbers into steps,
and for some customers two extra calls cross no step, or have a slightly
opposite effect in another branch. That is why the directional test's
threshold is chosen per model; for the forest, something like "it should
hold for 95 percent".

The last line is another behavioral test: the **obvious example** test.
For a customer who subscribed two months ago, called support six times
and barely uses the service, the model should give a high churn
probability. A few such obvious examples catch a big mistake in the
model quickly.

## Its place in the pipeline

Let's put it all together in GitHub Actions. First the code tests run;
if they pass, the model is trained and put through the gate:

```yaml
name: ML CI

on:
  pull_request:
    branches: [main]

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

  model-gate:
    needs: test
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python train.py
      - run: python check_quality.py
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: metrics
          path: metrics.json
```

What is new in this workflow:

- The `model-gate` job depends on `test` (`needs`): if the code tests
  fail, the model is never trained and the machine doesn't run for
  nothing.
- Training in CI is done with **small and fixed** data: the seeds are
  fixed, the time is a few minutes (`timeout-minutes` is its limit). The
  real, large training runs elsewhere; the purpose of training in CI is to
  quickly answer "did this change break the model?".
- The measurements (`metrics.json`) are kept in every case with
  `if: always()`: they are needed most when the gate fails, to see **why**
  it failed.

## Where do we get the bar from?

In this section we wrote the thresholds by hand (0.78). Better still is
to take the bar **from the model in production**: in the Model Registry
section's registry, the measurement of the `production` alias is stored.
If the gate asks "is the new model worse than the one in production?",
the threshold rises on its own as the model improves. Both are used
together too: a fixed floor (nobody may drop below it) and a comparison
with production.

## Summary

- In an ML pipeline, the **data**, the **model** and its **behavior** are
  tested along with the code.
- The feature function is tested with unit tests; the order of the
  columns too.
- **Quality gate:** a floor, a margin over the baseline, and a separate
  bar in every **slice** (customer group). It catches a model that broke
  while the code runs without errors.
- **Behavioral tests:** the directional test (does the prediction move in
  the expected direction when a value grows) and the obvious example test.
  The threshold is chosen per model.
- Training in CI is small, fixed and fast; the measurements are kept in
  every case.
- The bar is best taken from the model in production.
