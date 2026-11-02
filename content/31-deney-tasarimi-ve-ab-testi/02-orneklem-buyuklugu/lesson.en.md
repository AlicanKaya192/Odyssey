# Sample Size

In the Power Analysis section we answered "how many people are needed?"
with `solve_power`. This section puts the same calculation inside an
experiment plan: which metric, which effect, which traffic, how many weeks?
Most of the decisions that settle a test's result are made here, before the
test starts.

## The same relative effect, very different costs

Say the shop wants to see a **5% relative rise** in each metric. The people
needed for each metric (per group, 80% power, α = 0.05):

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower
from ab_data import make_user_log

users = make_user_log()
solver = TTestIndPower()
needed = {}
for col in ["bought", "minutes", "revenue"]:
    mean, sd = users[col].mean(), users[col].std()
    d = 0.05 * mean / sd
    n = solver.solve_power(effect_size=d, power=0.8, alpha=0.05)
    needed[col] = int(np.ceil(n))
    print(col, round(mean, 3), round(sd, 3), needed[col])
```

```text
bought 0.117 0.322 47209
minutes 21.096 23.273 7643
revenue 11.413 49.344 117372
```

For the same 5%, the time metric needs 7,643 people per group,
buying 47,209, revenue 117,372. The difference comes from
the coefficient of variation in The Experiment Question and Choosing a
Metric section: the effect size is $d = 0.05 \cdot \bar{x} / s$ and n grows
with $1/d^2$. Revenue may be the business's real goal, but making it the
primary metric can be very expensive.

## Mental arithmetic: the rule of 16

For 80% power and α = 0.05, comparing two groups, roughly:

$$n \approx \frac{16\, s^2}{\delta^2}$$

$\delta$ is the absolute difference you want to catch, $s$ the metric's
deviation. For buying:

```python
mean, sd = users["bought"].mean(), users["bought"].std()
delta = 0.05 * mean
print(int(np.ceil(16 * sd**2 / delta**2)))
```

```text
48117
```

Very close to `solve_power`. Where does 16 come from?
$2 \cdot (1.96 + 0.84)^2 \approx 15.7$: 1.96 standard deviations for a
two-sided 5% and 0.84 for 80% power. Enough for an estimate without a
computer in a planning meeting.

## What can we see with the traffic we have?

The question is often asked the other way round: 3000 different users come
each day and the test will run for two weeks. Which effect can we see with
80% power? This is the **minimum detectable effect** (MDE):

```python
n_group = 3000 * 14 // 2
d_min = solver.solve_power(nobs1=n_group, power=0.8, alpha=0.05)
for col in ["bought", "minutes", "revenue"]:
    mean, sd = users[col].mean(), users[col].std()
    print(col, f"{d_min * sd / mean:.1%}")
```

```text
bought 7.5%
minutes 3.0%
revenue 11.8%
```

In two weeks even a small change in the time metric is visible, but in
revenue only a rise of about 11.8% is reliably caught. If the
team hopes for a 2% rise in revenue, this test has failed before it starts:
either the duration grows, the metric changes or the variance is reduced
(the CUPED section).

## Unequal splits

A risky change may be shown to only a small part of the traffic. But to
keep the same power the total number of people grows:

```python
d = 0.05 * mean / sd
for share_b in [0.5, 0.2, 0.1]:
    ratio = share_b / (1 - share_b)
    n_a = solver.solve_power(effect_size=d, power=0.8, alpha=0.05,
                             ratio=ratio)
    n_a = int(np.ceil(n_a))
    n_b = int(np.ceil(n_a * ratio))
    print(share_b, n_a, n_b, n_a + n_b)
```

```text
0.5 47209 47209 94418
0.2 118022 29506 147528
0.1 236041 26227 262268
```

`ratio` is the B group's size relative to A. For a 20% B the total is about
56% more than 50/50, for a 10% B about 2.8
times. The small group sets the calculation: its noise stays large, so
growing the other group helps only a little.

## From people to weeks

```python
def weeks_needed(n_per_group, daily_users, traffic=1.0):
    days = 2 * n_per_group / (daily_users * traffic)
    return int(np.ceil(days / 7))


print(weeks_needed(needed["bought"], 3000),
      weeks_needed(needed["bought"], 3000, traffic=0.5),
      weeks_needed(needed["revenue"], 3000))
```

```text
5 9 12
```

- The duration is rounded to **full weeks**: weekday and weekend behaviour
  differ, and half a week over-represents some days.
- `traffic` is the share of traffic entering the experiment: if other
  experiments are running, or only visitors to the checkout page count, it
  shrinks and the duration grows.
- "3000 different users a day" is an optimistic assumption: as the same
  people come back, the number of new users grows more slowly than daily
  visits. The unit counted is the user, not the visit.

## Summary

- The people needed for the same relative effect grow with the square of
  the metric's coefficient of variation; revenue is expensive, the buying
  rate cheaper.
- $n \approx 16 s^2 / \delta^2$ is roughly right as mental arithmetic.
- With fixed traffic the MDE is computed; if it is larger than the hoped-for
  effect, the plan changes.
- Unequal splits increase the total number of people.
- The duration is rounded to full weeks; the unit counted is the user.
