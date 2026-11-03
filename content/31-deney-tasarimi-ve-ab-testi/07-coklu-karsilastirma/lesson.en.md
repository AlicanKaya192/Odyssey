# Multiple Comparisons

An A/B test dashboard never holds a single metric: buying, revenue,
basket size, clicks, session length, refunds... Each gets its own test,
and each carries a 5% chance of a false alarm. This section measures why
reading many tests at once is dangerous and shows three correction
methods.

## Twenty metrics, five "significant" results

Picture a dashboard that watches one experiment through 20 metrics. We
made the data, so we know the truth: B really changes only the first
three metrics (`metric_01` by 3%, `metric_02` by 2%, `metric_03` by
1.5%); the other 17 metrics have no effect at all.

```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from ab_data import make_metric_panel

panel = make_metric_panel()
metrics = [c for c in panel.columns if c.startswith("metric_")]


def metric_p(table):
    values = table[metrics].to_numpy()
    is_b = (table["group"] == "B").to_numpy()
    result = stats.ttest_ind(values[is_b], values[~is_b], equal_var=False)
    return result.pvalue


p = metric_p(panel)
print(*[m for m, x in zip(metrics, p) if x < 0.05])
```

```text
metric_01 metric_02 metric_03 metric_06 metric_20
```

Five metrics are below the 5% threshold. Three are real, but **two**
(`metric_06` and `metric_20`) are chance. Someone looking at the
dashboard reads those two as "B changed this too".

## Why does it happen?

In a single test, if H₀ is true the chance of a false alarm is 5%. Across
20 independent tests the chance of **at least one** false alarm is

$$1 - 0.95^{20} \approx 0.64$$

Let us measure it on 300 A/A dashboards where no metric changes:

```python
any_alarm = 0
for s in range(300):
    p_aa = metric_p(make_metric_panel(seed=1000 + s, effect=False))
    any_alarm += (p_aa < 0.05).any()
print(any_alarm / 300, round(1 - 0.95 ** 20, 3))
```

```text
0.66 0.642
```

In 66.0% of the dashboards where nothing changed, at least one
metric comes out "significant"; the formula says 64.2%. This is
called the **family-wise error rate** (FWER): the probability of at least
one false alarm in a family of tests. In the Peeking Trap and Sequential
Testing section, reading the same test every day was the same problem;
here we read the same day through 20 metrics.

## Three corrections

`statsmodels` offers three common methods through one function:

- **Bonferroni:** compare each p with α / m (m is the number of tests).
  The simplest and the strictest.
- **Holm:** sort the ps from smallest to largest; compare the smallest
  with α / m, the second with α / (m − 1)... and stop at the first one that
  fails. It protects the family-wise error rate as well as Bonferroni but
  never finds less.
- **Benjamini–Hochberg (BH):** protects something else: the **false
  discovery rate** (FDR), the expected share of false ones among the
  metrics called "significant". It compares the k-th sorted p with
  k · α / m and accepts everything up to the largest k that passes.

```python
for method in ["bonferroni", "holm", "fdr_bh"]:
    reject = multipletests(p, alpha=0.05, method=method)[0]
    print(method, *[m for m, r in zip(metrics, reject) if r])
```

```text
bonferroni metric_01
holm metric_01
fdr_bh metric_01
```

All three methods remove the two false alarms, but the truly affected
`metric_02` and `metric_03` go too: on this dashboard only the largest
effect remains. Correcting has a price.

## Measuring the price

A decision is not made by looking at one dashboard. Let us compare four
rules on 300 A/A dashboards (false alarms) and on 300 dashboards where the
first three metrics really change (real and false findings):

```python
methods = ["none", "bonferroni", "holm", "fdr_bh"]


def rejects(p_values, method):
    if method == "none":
        return p_values < 0.05
    return multipletests(p_values, alpha=0.05, method=method)[0]


alarm = {m: 0 for m in methods}
found = {m: [] for m in methods}
for s in range(300):
    p_aa = metric_p(make_metric_panel(seed=5000 + s, effect=False))
    p_ab = metric_p(make_metric_panel(seed=3000 + s))
    for m in methods:
        alarm[m] += rejects(p_aa, m).any()
        r = rejects(p_ab, m)
        found[m].append([r[:3].sum(), r[3:].sum()])
for m in methods:
    real, false = np.mean(found[m], axis=0)
    print(m, round(alarm[m] / 300, 3), round(real, 2), round(false, 2))
```

```text
none 0.657 2.45 0.85
bonferroni 0.057 1.65 0.06
holm 0.057 1.67 0.06
fdr_bh 0.057 1.89 0.16
```

The columns: at least one false alarm on A/A dashboards, how many of the
three real effects were found on average on the real dashboards, and how
many false metrics came out "significant".

- Reading without correction alarms on 65.7% of the A/A
  dashboards and adds 0.85 false metrics on average to every
  real dashboard.
- Bonferroni and Holm bring false alarms down to about 5%; in exchange
  they find 1.65 and 1.67 of the three real effects
  on average.
- BH sits in between: it finds 1.89 real effects, but
  0.16 false metrics on average also enter the dashboard. On an
  A/A dashboard every H₀ is true, so FDR and FWER are the same thing; that
  is why BH also stays near 5% there.

Which one to choose? It depends on how expensive a false "significant"
is. Where every finding turns into a product decision, Holm; in an
exploratory study that picks "worth a look" candidates from many metrics,
BH.

## The best correction: fewer questions

Correction methods only limit the damage. The real cure is the plan from
the Experiment Question and Choosing a Metric section:

- **One primary metric** is written in advance; the decision follows it,
  and it needs no correction.
- Guardrail metrics are read as "did it break"; secondary metrics do not
  decide, they only explain.
- Several variants (A/B/C/D) are multiple comparisons too: comparing each
  variant with the control runs three tests.
- Searching for metrics or segments after the test ends (the Segments and
  Simpson's Paradox section) is the same trap: whoever searches long
  enough finds a "significant" one.

## Summary

- With m tests, the probability of at least one false alarm is
  1 − (1 − α)^m; about 64% for 20 tests.
- Bonferroni and Holm protect the family-wise error rate, BH the false
  discovery rate.
- Correcting also misses real effects; its price is measured by
  simulation.
- The best cure is one primary metric written in advance.
