# Data Validation

Every month new customer data arrives and the model is retrained on it.
One month, the team that prepares the data starts sending the fees in
cents. Nobody says a word. The training code runs, the model is saved,
the pipeline is green. But the model is now worse. In this section we
see how to catch broken data before it reaches training: this is called
**data validation**.

## Broken data slips through silently

First let's write a small function that trains on clean data and
measures on the test set. The test set is always the same:
`make_customers(500, seed=99)`.

```python
from sklearn.ensemble import RandomForestClassifier
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X_test, y_test = to_xy(make_customers(500, seed=99))


def evaluate(rows):
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    model.fit(*to_xy(rows))
    return round(model.score(X_test, y_test), 3)


print("clean batch:", evaluate(make_customers(2000)))
```

```text
clean batch: 0.79
```

Now let's break the same data in three different ways. These are common
mistakes in real projects:

- The fee arrives in cents (2990 instead of 29.90).
- The plan name is written in capitals (`"PRO"` instead of `"pro"`).
- Usage hours are empty (`None`) in some rows.

```python
cents = make_customers(2000)
for row in cents:
    row["monthly_fee"] = round(row["monthly_fee"] * 100)
print("fees in cents:", evaluate(cents))

upper = make_customers(2000)
for row in upper:
    row["plan"] = row["plan"].upper()
print("plan in capitals:", evaluate(upper))

holes = make_customers(2000)
for row in holes[::10]:
    row["usage_hours"] = None
print("empty usage:", evaluate(holes))
```

```text
fees in cents: 0.744
plan in capitals: 0.78
empty usage: 0.782
```

**Not one of them raised an error.** With the fees in cents, the
accuracy fell from 0.79 to 0.744: the model
learned rules for large numbers, and the real fees in the test set fit
none of those rules. The plan name in capitals is not equal to `"pro"`
in `to_xy`, so every customer was counted as `basic`. As for the empty
values, scikit-learn's trees can handle them on their own; silent
again.

This is where the danger lies: if the code had failed, we would have
noticed at once. A data mistake usually doesn't stop the code; it only
makes the model worse. That is why we must check the data ourselves
**before training**.

## Rules: the data contract

First let's write down what the data should look like. One rule per
column: which range the numbers must fall in, which values the texts may
take. This set of rules is called a **schema**, or a **data contract**,
because it is an agreement between whoever sends the data and whoever
receives it:

```python
SCHEMA = {
    "tenure": {"min": 1, "max": 72},
    "monthly_fee": {"min": 5, "max": 100},
    "support_calls": {"min": 0, "max": 10},
    "usage_hours": {"min": 0, "max": 100},
    "plan": {"allowed": ["basic", "pro"]},
    "churned": {"allowed": [0, 1]},
}


def check_row(row, schema):
    problems = []
    for column, rule in schema.items():
        value = row.get(column)
        if value is None:
            problems.append(f"{column}: missing")
        elif "allowed" in rule:
            if value not in rule["allowed"]:
                problems.append(f"{column}: {value!r} is not allowed")
        elif not isinstance(value, (int, float)):
            problems.append(f"{column}: {value!r} is not a number")
        elif not rule["min"] <= value <= rule["max"]:
            problems.append(f"{column}: {value} is out of range")
    return problems


row = make_customers(1)[0]
print("clean row:", check_row(row, SCHEMA))
bad = {**row, "tenure": -3, "monthly_fee": "29.90", "usage_hours": None, "plan": "PRO"}
for problem in check_row(bad, SCHEMA):
    print(problem)
```

```text
clean row: []
tenure: -3 is out of range
monthly_fee: '29.90' is not a number
usage_hours: missing
plan: 'PRO' is not allowed
```

`check_row` asks every column four questions in order:

1. **Is there a value?** `row.get(column)` also gives `None` if the
   column is missing altogether; a missing column and an empty value end
   up in the same place.
2. **Is it one of the allowed values?** Only for columns with an
   `allowed` rule.
3. **Is it a number?** `"29.90"` is in quotes, so it is text; it looks
   like a number but it isn't one. `isinstance(value, (int, float))`
   asks whether the value is one of these two types.
4. **Is it in range?** `min <= value <= max`.

The clean row gives an empty list: no problems at all. `{value!r}`
writes the value in its `repr` form, that is, text with its quotes:
when you see `'PRO'` in the output, you know it is text.

## Checking a batch

Data doesn't arrive row by row but as a **batch**: this month's 1000
customers, for example. Let's count how many problems each column has in
a batch. First let's break a batch: the plan name is in capitals in one
row out of every 40, and usage hours are empty in one row out of every
25.

```python
from collections import Counter

batch = make_customers(1000, seed=21)
for i, row in enumerate(batch):
    if i % 40 == 0:
        row["plan"] = row["plan"].upper()
    if i % 25 == 0:
        row["usage_hours"] = None


def report(rows, schema):
    counts = Counter()
    bad_rows = 0
    for row in rows:
        problems = check_row(row, schema)
        if problems:
            bad_rows += 1
        for problem in problems:
            counts[problem.split(":")[0]] += 1
    return bad_rows, counts


bad_rows, counts = report(batch, SCHEMA)
print("bad rows:", bad_rows, "of", len(batch))
for column, n in counts.most_common():
    print(" ", column, n)
```

```text
bad rows: 60 of 1000
  usage_hours 40
  plan 25
```

The number of bad rows is smaller than the sum of the two problems,
because some rows have both (the row numbers divisible by both 40 and
25). The report also says **where** the problem is: the usage hours and
the plan name. That is exactly the information to take to the team that
sends the data.

## Quarantine or reject?

We found the problem rows. Now what? There are two ways:

- **Quarantine:** set the bad rows aside, keep them for inspection, and
  carry on with the sound rows. The right choice for a few rows entered
  wrongly now and then.
- **Reject:** turn the whole batch back. If the share of bad rows is
  large, something has broken systematically; there may be other errors
  the rules didn't catch. Training on that batch is risky.

Let's write a **gate** that combines the two: quarantine the bad rows,
but reject the batch if their share goes over a limit.

```python
def gate(rows, schema, max_bad_share=0.05):
    good, quarantine = [], []
    for row in rows:
        if check_row(row, schema):
            quarantine.append(row)
        else:
            good.append(row)
    share = len(quarantine) / len(rows)
    if share > max_bad_share:
        raise ValueError(f"batch rejected: {share:.1%} of the rows are bad")
    return good, quarantine


try:
    gate(batch, SCHEMA)
except ValueError as error:
    print(error)

small = make_customers(1000, seed=22)
small[10]["tenure"] = 0
small[20]["plan"] = "gold"
good, quarantine = gate(small, SCHEMA)
print("accepted:", len(good), "quarantined:", len(quarantine))
```

```text
batch rejected: 6.0% of the rows are bad
accepted: 998 quarantined: 2
```

In the first batch the share of bad rows went over the limit and the
gate **raised an error** (`raise`). This is done on purpose: the
training script cannot continue past the gate, the script ends with an
error code and, as you saw in the CI/CD and DevOps module, the pipeline
turns red. In the second batch only two rows are bad; they were
quarantined and training can go on with the remaining rows.

`if check_row(row, schema):` counts a non-empty list as `True`: if there
is at least one problem, the row goes to quarantine.

## Damage the rules cannot see

The rules look at values one by one. What if every value is valid on its
own but the data is still wrong? Say the system that keeps the support
records broke this month and every customer's support calls came in as
`0`. `0` is a valid value; no rule objects. But when measured, this
breaks the model too: a model trained on 2000 customers broken the same
way has an accuracy of 0.744 (with clean data
0.79).

To catch this, we look not at single values but at the column **as a
whole**. From the training data we take a **profile**: the mean and the
standard deviation of every numeric column. We measure how far the new
batch's mean has moved from the training mean. Writing the distance in
standard deviations lets us compare all the columns on the same scale:

```python
import statistics


def profile(rows, columns):
    result = {}
    for column in columns:
        values = [row[column] for row in rows if row[column] is not None]
        result[column] = {"mean": statistics.mean(values),
                          "std": statistics.pstdev(values)}
    return result


def compare(reference, rows, columns, limit=0.5):
    new = profile(rows, columns)
    for column in columns:
        old = reference[column]
        shift = abs(new[column]["mean"] - old["mean"]) / old["std"]
        status = "CHECK" if shift > limit else "ok"
        print(f"{column:14} {shift:.2f}  {status}")


reference = profile(make_customers(2000), NUMERIC)
print("normal batch")
compare(reference, make_customers(1000, seed=21), NUMERIC)
lost = make_customers(1000, seed=21)
for row in lost:
    row["support_calls"] = 0
print("calls lost")
compare(reference, lost, NUMERIC)
print("bad rows by the rules:", report(lost, SCHEMA)[0])
```

```text
normal batch
tenure         0.01  ok
monthly_fee    0.02  ok
support_calls  0.01  ok
usage_hours    0.02  ok
calls lost
tenure         0.01  ok
monthly_fee    0.02  ok
support_calls  0.68  CHECK
usage_hours    0.02  ok
bad rows by the rules: 0
```

In the normal batch all the shifts are very small: it is just another
batch from the same customers. In the batch that lost its support calls,
the `support_calls` column moved by 0.68 standard
deviations and was flagged. In the same batch the rules found **not a
single** bad row. The two checks complement each other:

- **Rules** catch errors in single values: missing, wrong type, out of
  range, not allowed.
- **Profile comparison** catches a change in the column as a whole:
  every value is valid but the distribution is wrong.

A profile comparison is a warning, not a verdict: the customers may
really have changed. "CHECK" says a person should take a look. In the
Data Drift section we will measure how data changes over time after
release with sturdier methods.

## Its place in the pipeline

Validation runs before training, as a separate step of the pipeline:

<figure class="fig">
  <div class="flow">
    <span class="node">New data</span>
    <span class="arrow">→</span>
    <span class="node acc">Rule checks</span>
    <span class="arrow">→</span>
    <span class="node acc">Profile comparison</span>
    <span class="arrow">→</span>
    <span class="node">Training</span>
    <span class="arrow">→</span>
    <span class="node">Evaluation</span>
  </div>
  <figcaption>If the gate is not passed, training never starts.</figcaption>
</figure>

The same rules are useful **at prediction time** too: if a request to
the model has the plan name `"PRO"`, returning a clear error is better
than silently giving a wrong prediction. In the Writing REST APIs with FastAPI module,
Pydantic turning a bad request back with `422` is the same idea. It
matters that the checks in training and in prediction are the same; we
will come back to this in the Training-Serving Skew section.

## Where do the rules come from?

You find the numbers in the schema in two places:

- **Domain knowledge:** if the service started at most 72 months ago,
  tenure cannot be over 72. The plan can only be `basic` or `pro`. These
  rules are written together with the team that sends the data; that is
  where the word contract comes from.
- **Reference data:** the smallest and largest values and the categories
  seen in trusted training data. This way is quick but can be too narrow:
  if the highest fee in training is 58, a real customer paying 60 is
  rejected. That is why a margin is left on the inferred range and a
  person reviews the rules.

In real projects there are libraries that make this easier (such as
pandera and Great Expectations): you write the schema and the table is
checked on every batch. The idea is the same as what we wrote in this
section.

## Summary

- A data mistake usually **doesn't stop the code**; it only makes the
  model worse. That is why data is checked before training.
- A **schema** (data contract) writes down every column's rule: range,
  allowed values, not missing.
- In a batch, problems are counted column by column; the report says
  where the problem is.
- A few bad rows are **quarantined**; if the share of bad rows is large,
  the batch is **rejected** and the pipeline stops.
- The distribution can be broken while every value is valid: compare the
  new batch's **profile** with the training data's.
- Rules come from domain knowledge and from reference data; leave a
  margin on inferred ranges.
