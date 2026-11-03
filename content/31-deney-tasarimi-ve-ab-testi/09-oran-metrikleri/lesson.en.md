# Ratio Metrics and the Delta Method

Some metrics are the ratio of two totals: click-through rate (clicks /
views), revenue per order (revenue / orders), time per session. These
metrics hide a trap: what is **assigned** in the experiment is the user,
but the ratio's denominator is not the user, it is the view. This section
measures why a test that forgets this gives too many alarms and shows the
**delta method**, which gives the right standard error.

## Many views per user

In a page design test every user sees a few pages and clicks on some. The
metric is the click-through rate (CTR): total clicks / total views. In
this data B has no effect at all (A/A).

```python
import numpy as np
from scipy import stats
from ab_data import make_pageviews

views = make_pageviews()
sums = views.groupby("group")[["pageviews", "clicks"]].sum()
print(sums)
print(round(views["pageviews"].mean(), 2))
```

```text
       pageviews  clicks
group                   
A          25368    1676
B          24035    1572
8.23
```

Each group has about 3000 users but 25,368 and 24,035
views; 8.23 views per user on average.

## The naive test: counting every view as independent

The two-proportion z-test from the Comparing Proportions section treats
every trial as independent. If we give it the views as trials:

```python
def naive_test(table):
    s = table.groupby("group")[["pageviews", "clicks"]].sum()
    r = s["clicks"] / s["pageviews"]
    se = np.sqrt((r * (1 - r) / s["pageviews"]).sum())
    z = (r["B"] - r["A"]) / se
    return round(float(se), 5), round(float(2 * stats.norm.sf(abs(z))), 4)


print(naive_test(views))
```

```text
(0.00223, 0.7663)
```

But the views of the same user are not independent: some users click on
almost everything, some never click. When ten views of one user count as
ten separate people, the sample looks larger than it is and the standard
error comes out smaller than it is.

## The delta method

The right unit is the user. Let each user's clicks be Y and views X; the
ratio is R = Ȳ / X̄ (the ratio of the means, that is, the ratio of the
totals). For the ratio of two means, the **delta method** gives this
variance:

$$\operatorname{var}(R) \approx \frac{1}{n\,\bar{X}^2}\left(s_Y^2 - 2R\,s_{XY} + R^2 s_X^2\right)$$

Here n is the number of users, s² are variances and s_XY is the
covariance; all are computed **at the user level**.

```python
def delta_test(table):
    parts = {}
    for g in ["A", "B"]:
        t = table[table["group"] == g]
        x = t["pageviews"].to_numpy(dtype=float)
        y = t["clicks"].to_numpy(dtype=float)
        r = y.mean() / x.mean()
        cov = np.cov(x, y)[0, 1]
        var = (y.var(ddof=1) - 2 * r * cov + r ** 2 * x.var(ddof=1))
        parts[g] = (r, var / (len(x) * x.mean() ** 2))
    se = np.sqrt(parts["A"][1] + parts["B"][1])
    z = (parts["B"][0] - parts["A"][0]) / se
    return round(float(se), 5), round(float(2 * stats.norm.sf(abs(z))), 4)


print(delta_test(views))
```

```text
(0.00278, 0.8116)
```

The delta method's standard error is 1.25 times the naive
test's. In this example both tests say "no difference"; so when does the
difference matter?

## By simulation: the naive test alarms too often

Let us count the false alarm rate of both tests on 400 A/A experiments:

```python
alarms = np.zeros(2)
for s in range(400):
    t = make_pageviews(seed=6000 + s)
    alarms += [naive_test(t)[1] < 0.05, delta_test(t)[1] < 0.05]
print(np.round(alarms / 400, 3))
```

```text
[0.132 0.06 ]
```

The naive test says "significant" in 13.2% of the experiments
where nothing changed: far above the promised 5%. The delta method stays
near 5% with 6.0%.

## Checking with the bootstrap

As we saw in the Bootstrap and the Permutation Test section, resampling is
done **at the unit of assignment**. Let us resample users (together with
their clicks and views) and look at how much group A's ratio moves:

```python
a = views[views["group"] == "A"]
x = a["pageviews"].to_numpy()
y = a["clicks"].to_numpy()
rng = np.random.default_rng(901)
ratios = []
for _ in range(2000):
    i = rng.integers(0, len(x), len(x))
    ratios.append(y[i].sum() / x[i].sum())
r = y.sum() / x.sum()
delta_se = np.sqrt((y.var(ddof=1) - 2 * r * np.cov(x, y)[0, 1]
                    + r ** 2 * x.var(ddof=1)) / (len(x) * x.mean() ** 2))
print(round(float(np.std(ratios)), 5), round(float(delta_se), 5))
```

```text
0.00199 0.00202
```

The user-level bootstrap and the delta method give the same standard
error. The delta method finds with one formula what the bootstrap finds
with thousands of repetitions; that is why it is common on large
experimentation platforms.

## Two different "average rates"

A ratio metric can be defined two ways, and they ask different questions:

- **The ratio of totals** (Σ clicks / Σ views): every view weighs the
  same; a user with many views moves the rate more. It needs the delta
  method.
- **The mean of user rates** (the average of each user's clicks / views):
  every user weighs the same. This is already a user-level metric; an
  ordinary Welch test is enough.

Which one is reported is written in advance, as in the Experiment Question
and Choosing a Metric section.

## Summary

- When the unit of assignment (user) and the metric's denominator (view)
  differ, the views are not independent.
- A test that counts views as independent finds a standard error that is
  too small and gives too many alarms.
- The delta method computes the ratio's variance from user-level
  variances and covariances.
- A user-level bootstrap gives the same result.
