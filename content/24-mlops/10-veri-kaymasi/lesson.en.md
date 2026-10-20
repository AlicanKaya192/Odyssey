# Data Drift

In the Monitoring section a column's mean shifted from month to month and
the predicted rate climbed. The mean is a crude measure: the shape of a
distribution can change while the mean stays put. In this section we
write two common methods ourselves that measure how much a column's
distribution has changed: **PSI** and **KS**. Then we look at two
important questions: why does a "significant" difference mislead on big
data, and does every drift harm the model?

## What is data drift?

If the distribution of the model's inputs changes over time, this is
called **data drift**. In this module's data, as the months pass,
customers use the service less and pay more. The model is the same; the
customers it sees change.

A comparison has two sides: the **reference** (the data the model was
trained on) and the **current** data (this month's).

```python
from ml_data import make_customers, NUMERIC

reference = make_customers(2000)


def column(rows, name):
    return [r[name] for r in rows]


def month_rows(month):
    return make_customers(1000, seed=99, month=month)


print("reference usage:", round(sum(column(reference, "usage_hours")) / 2000, 1))
print("month 3 usage:", round(sum(column(month_rows(3), "usage_hours")) / 1000, 1))
```

```text
reference usage: 32.2
month 3 usage: 27.5
```

## PSI: binning and comparing

**PSI** (population stability index) works like this:

1. Sort the reference data and split it into ten **equally crowded** bins:
   each bin holds 10 percent of the reference. The bin edges are the
   reference's deciles.
2. Compute the share of the current data that falls into each bin.
3. For every bin, `(current - reference) × ln(current / reference)`, and
   add them up.

If the shares are the same, every term is zero; the more they differ, the
bigger the PSI.

```python
import bisect
import math


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


print("month  " + "  ".join(f"{name:>13}" for name in NUMERIC))
for month in [0, 1, 2, 3, 6]:
    current = month_rows(month)
    values = [psi(column(reference, n), column(current, n)) for n in NUMERIC]
    print(f"{month:>5}  " + "  ".join(f"{v:>13.3f}" for v in values))
```

```text
month         tenure    monthly_fee  support_calls    usage_hours
    0          0.012          0.013          0.004          0.016
    1          0.030          0.058          0.026          0.037
    2          0.005          0.229          0.055          0.121
    3          0.012          0.456          0.109          0.284
    6          0.012          1.875          0.280          1.152
```

Three details in the code:

- `edges` are the nine bin edges: the values at one tenth, two tenths...
  of the sorted list.
- `bisect.bisect_left(edges, v)` finds which bin a value falls into: the
  bin numbered by how many edges are smaller than `v`. It is a fast
  function that looks up a position in a sorted list.
- In an empty bin the share is zero and `log(0)` is undefined; that is why
  we make every share at least `0.0001`.

When reading the table, a common rule of thumb (not a law):

| PSI | Reading |
|---|---|
| Below 0.1 | Stable |
| 0.1 – 0.25 | Moderate drift, take a look |
| Above 0.25 | Large drift |

The month 0 row matters: it is **another sample** from the same month.
Although nothing changed, the PSI is not zero (around 0.01): the
luck of the sample. A drift is meaningful when it is clearly above this
noise level. The fee shows a large drift from month 2 on, usage from
month 3 on; tenure doesn't drift at all.

## KS: the largest gap

The second method is the **Kolmogorov-Smirnov** (KS) test. For both
datasets it draws the curve "what share of the values is less than or
equal to `x`?" (the cumulative distribution) and looks at the **largest
vertical distance** between the two curves. That distance is the KS
**statistic**: between 0 and 1, near zero for identical distributions.
Let's write it ourselves and compare it with SciPy's:

```python
from scipy.stats import ks_2samp


def ks_statistic(a, b):
    a, b = sorted(a), sorted(b)
    gaps = []
    for x in sorted(set(a) | set(b)):
        share_a = bisect.bisect_right(a, x) / len(a)
        share_b = bisect.bisect_right(b, x) / len(b)
        gaps.append(abs(share_a - share_b))
    return max(gaps)


ref_usage = column(reference, "usage_hours")
month1_usage = column(month_rows(1), "usage_hours")
print("ours:", round(ks_statistic(ref_usage, month1_usage), 4))
print("scipy:", round(float(ks_2samp(ref_usage, month1_usage).statistic), 4))
```

```text
ours: 0.0805
scipy: 0.0805
```

The two are the same. `bisect_right(a, x)` gives how many values in the
sorted list are less than or equal to `x`; divided by the list's length,
it is a share. The union of the sets (`|`) walks every value of the two
datasets once.

## The p-value trap

`ks_2samp` also gives a **p-value**: "if the two samples came from the
same distribution, how often would a difference this large appear?" If it
is small, the difference is called "statistically significant". But the
p-value shrinks as the sample grows. Let's measure the same small drift
(usage from month 0 to month 1) at three different sizes:

```python
for n in [200, 2000, 50000]:
    a = column(make_customers(n, seed=1), "usage_hours")
    b = column(make_customers(n, seed=2, month=1), "usage_hours")
    result = ks_2samp(a, b)
    statistic, p_value = result.statistic, result.pvalue
    print(f"n={n:>6}  statistic {statistic:.3f}  p-value {p_value:.2g}")
```

```text
n=   200  statistic 0.095  p-value 0.33
n=  2000  statistic 0.083  p-value 2.1e-06
n= 50000  statistic 0.076  p-value 1.2e-124
```

The size of the drift (the statistic) is about the same in all three
rows. The p-value, though, is "not significant" with 200 customers and
absurdly "significant" with 50,000. Live systems have a lot of data; an
alert that looks at the p-value goes off at even the smallest,
unimportant drift. That is why monitoring uses **measures of size** (PSI,
the KS statistic) and puts the threshold on them.

`:.2g` writes a number with two significant digits; very small numbers in
exponent form (`1.2e-124`).

## Does every drift do harm?

Remember the accuracy table from the Monitoring section. The fee's PSI in
month 3 is 0.456: a "large drift" by the table. The model's
accuracy that month, though, is still 0.784, close to training.
Accuracy only dropped in month 4.

Why? Because in this module's data, although the fee and usage change,
**how** customers decide stays the same until month 4: a high fee and
little usage still lead to cancelling at the same rate. The model learned
this relationship; as long as the relationship holds, it predicts
correctly even when the inputs drift. What changes in month 4 is the
relationship itself; that is the topic of the next section: **concept
drift**.

That is why:

- Data drift is a **warning**, not a reason to retrain on its own.
- Look first at drift in the columns the model relies on most; a large
  drift in an unimportant column is often harmless.
- The real decision is made by the **quality** measured when the labels
  arrive.

## Categorical columns

PSI's bins are for numeric columns. In a categorical column such as the
plan, the bins are already there: every category is a bin. The same
formula is applied to the categories' shares. In this module's data the
`pro` share stays at about 40 percent through the months; the plan
doesn't drift.

## Summary

- **Data drift:** the distribution of the model's inputs changing over
  time.
- **PSI:** split the reference into equally crowded bins and compare the
  current shares. Below 0.1 stable, above 0.25 large drift (a rule of
  thumb).
- The PSI of another sample from the same month is not zero: know the
  noise level first.
- **KS statistic:** the largest distance between two cumulative
  distributions.
- The **p-value** makes every small difference look "significant" on big
  samples; monitoring uses a measure of size.
- Not every drift does harm: if the inputs drift but the relationship
  stays the same, the model stays good. The decision is made by quality.
