# Analysing Your First A/B Test

In the previous four sections we saw what it takes to set up a test: the
question and metric, random assignment, sample size and trust checks. Now
we analyse a finished test from start to finish. The order is always the
same: **trust checks first, then the primary metric, then secondary and
guardrail metrics, and finally the decision according to the plan.**

## The plan (written before the test started)

- Change: the checkout button moves to the top of the page.
- Primary metric: per-user buying rate (`bought`).
- Secondary metric: revenue per user (`revenue`).
- Guardrail metric: the refund rate among buyers; it must not rise.
- 50/50 split, two weeks, about 15,000 people per group.
- With this size the minimum detectable effect (MDE) at 80% power is about
  1.1 points.
- Practical threshold: moving the button is cheap, so a rise of **at least
  0.3 points** in buying is enough.
- Test: two-proportion z-test, two-sided, α = 0.05.

## 1. Trust check: SRM

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportions_ztest)
from ab_data import make_experiment

test = make_experiment()
n = test["group"].value_counts().sort_index()
print(n.to_dict(), round(stats.chisquare(n).pvalue, 3))
```

```text
{'A': 15041, 'B': 14959} 0.636
```

The SRM p is 0.636: the group sizes match the 50/50 design. There
is no sign of a loss like the one in the A/A Tests and Sample Ratio
Mismatch section.

## 2. Trust check: the balance table

Visits **before** the test and the platform cannot be affected by the
change; they should be similar in both groups:

```python
test["mobile"] = (test["platform"] == "mobile").astype(int)
print(test.groupby("group")[["sessions", "mobile"]].mean().round(3))
```

```text
       sessions  mobile
group                  
A         3.725   0.595
B         3.756   0.596
```

The groups are balanced. Now we can look at the result.

## 3. The primary metric

```python
k = test.groupby("group")["bought"].sum()
rate = k / n
p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print(rate.round(4).to_dict())
print(round(p, 4))
print(round(low, 4), round(high, 4))
```

```text
{'A': 0.1174, 'B': 0.1297}
0.0012
0.0048 0.0197
```

- The buying rate is 11.74% in A and 12.97% in B: a
  difference of 1.23 points (10.5% relative).
- p = 0.0012: the difference is very likely not chance.
- The 95% confidence interval is 0.48 – 1.97 points.

## 4. The secondary metric: revenue

```python
rev_a = test.loc[test["group"] == "A", "revenue"]
rev_b = test.loc[test["group"] == "B", "revenue"]
welch = stats.ttest_ind(rev_b, rev_a, equal_var=False)
print(round(rev_a.mean(), 2), round(rev_b.mean(), 2), round(welch.pvalue, 3))
```

```text
12.55 12.75 0.737
```

Revenue is a little higher in B but p = 0.74: in this test the
revenue difference cannot be told apart from noise. That does not mean
"revenue did not rise"; as we saw in The Experiment Question and Choosing a
Metric section, revenue is very noisy and a test of this size is not enough
to measure it. That is exactly why revenue was not made the primary metric.

## 5. The guardrail metric: refund rate

```python
buyers = test[test["bought"] == 1]
refund = buyers.groupby("group")["refunded"].agg(["sum", "count"])
print((refund["sum"] / refund["count"]).round(4).to_dict())
p_refund = proportions_ztest(refund["sum"].to_numpy(),
                             refund["count"].to_numpy())[1]
print(round(p_refund, 3))
```

```text
{'A': 0.0742, 'B': 0.0747}
0.948
```

The refund rate is almost the same in both groups (p = 0.95):
no sign of harm in the guardrail metric.

## 6. Deciding by the plan

The decision is made by rules written before the test:

```python
def decide(srm_p, guard_ok, low, threshold):
    if srm_p < 0.001:
        return "stop: SRM"
    if not guard_ok:
        return "stop: guardrail"
    if low >= threshold:
        return "ship"
    if low > 0:
        return "unclear"
    return "no evidence"


print(decide(stats.chisquare(n).pvalue, p_refund > 0.05, low, 0.003))
```

```text
ship
```

The lower end of the interval (0.48 points) is above the practical
threshold (0.3 points): the change is shipped.

## The report

"Moving the button to the top changed the buying rate from 11.74% to
12.97%: +1.23 points (95% confidence interval
0.48 – 1.97, p = 0.0012). The SRM and balance
checks are clean and the refund rate did not change. The revenue
difference could not be measured in this test. The change is being
shipped."

The report holds four things: the trust checks, the size of the effect and
its interval, the secondary and guardrail metrics, and a decision based on
the plan.

## Summary

- SRM and balance first, then the primary metric.
- In the primary metric the difference, interval and p are read together.
- A non-significant secondary metric does not mean "no effect" for a noisy
  metric.
- If a guardrail metric gets worse, the test stops even if the primary
  metric is good.
- The decision is made with rules written before the test.
