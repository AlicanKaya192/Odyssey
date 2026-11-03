# Capstone Project

In this section we analyse an experiment from start to finish, using every
step of the module. An online shop is thinking of lowering its
free-shipping limit. The question: **does this change raise buying, and
does it break something while doing so?** We made the data; let us not
say the true effect until the end, and let the analysis find it.

## 1. The plan (before the test)

As in the Experiment Question and Choosing a Metric section, the plan has
been written:

- **Primary metric:** the buying rate (per user, 0/1).
- **Practical threshold:** a rise of at least 0.3 points.
- **Secondary metric:** revenue per user (with CUPED, the covariate being
  spending in the four weeks before the test).
- **Guardrail metric:** the refund rate among buyers; a rise of more than 2
  points is not accepted.
- **Segment:** platform only (the single segment written in advance).
- **Sample:** a base rate of 10%, a smallest important difference of 1
  point.

```python
import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportion_effectsize,
                                          proportions_ztest)
from ab_data import make_capstone

h = proportion_effectsize(0.11, 0.10)
need = NormalIndPower().solve_power(h, alpha=0.05, power=0.8)
print(int(np.ceil(need)))
```

```text
14745
```

14,745 users are needed per group (the Sample Size section). The
test ran for two weeks and collected 40,000 users.

## 2. Trust checks

```python
test = make_capstone()
n = test.groupby("group").size()
print(n.to_dict(), round(stats.chisquare(n).pvalue, 3))
print(test.groupby("group")["pre_spend"].mean().round(2).to_dict())
```

```text
{'A': 19902, 'B': 20098} 0.327
{'A': 132.21, 'B': 131.59}
```

The SRM p is 0.327: far above the 0.001 threshold, the assignment
is sound (the A/A Tests and Sample Ratio Mismatch section). Spending before
the test is almost the same in both groups: the groups are balanced. Each
group has about 20,000 people, more than the 14,745 in the plan.

## 3. The primary metric

```python
k = test.groupby("group")["bought"].sum()
p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print((k / n).round(4).to_dict(), f"{p:.1e}")
print(round(low * 100, 2), round(high * 100, 2))
```

```text
{'A': 0.1007, 'B': 0.1154} 2.4e-06
0.86 2.07
```

Buying is 11.54% instead of 10.07%. The difference's 95%
interval is 0.86 to 2.07 points: entirely above the
0.3-point threshold.

## 4. The secondary metric: revenue, with CUPED

```python
y = test["revenue"].to_numpy()
x = test["pre_spend"].to_numpy()
is_b = (test["group"] == "B").to_numpy()
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
adjusted = y - theta * (x - x.mean())
for values in (y, adjusted):
    welch = stats.ttest_ind(values[is_b], values[~is_b], equal_var=False)
    diff = values[is_b].mean() - values[~is_b].mean()
    print(round(diff, 2), round(welch.pvalue, 4))
print(round(np.corrcoef(x, y)[0, 1], 2), round(adjusted.var() / y.var(), 3))
```

```text
1.01 0.0014
1.03 0.0009
0.21 0.957
```

Revenue per user is about 1.01 TL higher in B. The correlation of
spending before the test with revenue is only 0.21, so CUPED
removes only 4.3% of the variance (1 − ρ² from the Variance
Reduction: CUPED section). The gain is small but free; revenue still stays
a secondary metric.

## 5. The guardrail metric: refunds

```python
buyers = test[test["bought"] == 1]
refunds = buyers.groupby("group")["refunded"].agg(["sum", "count"])
print((refunds["sum"] / refunds["count"]).round(4).to_dict())
low_r, high_r = confint_proportions_2indep(
    refunds.loc["B", "sum"], refunds.loc["B", "count"],
    refunds.loc["A", "sum"], refunds.loc["A", "count"])
print(round(low_r * 100, 2), round(high_r * 100, 2))
```

```text
{'A': 0.0773, 'B': 0.0716}
-2.16 0.99
```

The top of the interval for the refund rate difference is 0.99
points: below the 2-point limit in the plan. The guardrail did not break.

## 6. The segment written in advance: platform

```python
for name, part in test.groupby("platform"):
    rates = part.groupby("group")["bought"].mean()
    print(name, round(rates["B"] / rates["A"] - 1, 3), len(part))
```

```text
desktop 0.169 17991
mobile 0.122 22009
```

B is ahead on both platforms. As we saw in the Segments and Simpson's
Paradox section these numbers are noisy; we do not interpret the gap
between them, we only say "the same direction on both platforms".

## 7. Decision and report

```python
def verdict(low, high, threshold=0.003):
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


srm_ok = stats.chisquare(n).pvalue > 0.001
guard_ok = high_r < 0.02
print(srm_ok, guard_ok, verdict(low, high))
```

```text
True True ship
```

The report:

> Lowering the free-shipping limit raised buying from 10.07% to
> 11.54% (95% interval 0.86 – 2.07 points, above
> the 0.3-point threshold written in advance). SRM and balance are clean,
> the refund rate is within the limit in the plan, and both platforms move
> in the same direction. The revenue rise is noted as a secondary metric.
> Decision: launching. Limits: a two-week test; a small holdout will be kept
> after launch for the novelty effect.

Since we made the data, we can also tell the truth: B really raised buying
by 12%; order sizes and refunds did not change. The analysis found this
correctly.

## Summary

- The plan comes before the test: metrics, thresholds, sample, segment.
- Trust first (SRM, balance), then the primary metric, then secondary and
  guardrail metrics.
- CUPED's gain depends on the correlation; here it is small.
- The decision follows rules written in advance, and the report is written
  together with its limits.
