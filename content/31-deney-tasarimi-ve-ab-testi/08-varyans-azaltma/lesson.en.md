# Variance Reduction: CUPED

In the Sample Size section we saw that the number of users needed is
proportional to the metric's variance. Catching a small effect in a noisy
metric needs either many users or much time. This section shows a third
way: explaining part of the noise with data collected **before** the
experiment and removing it. The method is called **CUPED** (Controlled
experiment Using Pre-Experiment Data).

## Where the noise comes from: users differ

We have a test that measures minutes spent in an app. B truly raises
minutes by 3%. But users already differ a lot: some stay two minutes a
day, some an hour. That difference does not come from B, it comes from
the person, and it drowns the difference of the means in noise.

```python
import numpy as np
from scipy import stats
from ab_data import make_engagement_test

test = make_engagement_test()
is_b = (test["group"] == "B").to_numpy()
minutes = test["minutes"].to_numpy()


def compare(y, b):
    diff = y[b].mean() - y[~b].mean()
    se = np.sqrt(y[b].var(ddof=1) / b.sum() + y[~b].var(ddof=1) / (~b).sum())
    p = 2 * stats.norm.sf(abs(diff / se))
    return round(float(diff), 3), round(float(se), 3), round(float(p), 4)


print(compare(minutes, is_b))
```

```text
(1.134, 0.355, 0.0014)
```

The difference is 1.13 minutes with a standard error of
0.355. The test is significant, but the interval is wide.

## The idea: behaviour before the experiment

We know the same users' minutes in the two weeks before the test
(`pre_minutes`). Someone who stays an hour stayed a lot before the test
too. Let us adjust every user's minutes with this information:

$$Y_{\text{cuped}} = Y - \theta\,(X - \bar{X}), \qquad \theta = \frac{\operatorname{cov}(X, Y)}{\operatorname{var}(X)}$$

Here X is the value before the experiment. θ is how much X explains Y
(the slope of a linear regression). Since X was measured **before**
assignment, its mean is the same in both groups; the adjustment does not
change the difference, it only reduces the noise.

```python
pre = test["pre_minutes"].to_numpy()


def cuped(y, x):
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return y - theta * (x - x.mean())


rho = np.corrcoef(pre, minutes)[0, 1]
adjusted = cuped(minutes, pre)
print(round(rho, 3), round(adjusted.var() / minutes.var(), 3))
print(compare(adjusted, is_b))
```

```text
0.75 0.437
(1.04, 0.235, 0.0)
```

The correlation of the minutes before and during is 0.75. After
the adjustment only 44% of the variance is left; this is the
same as what the formula 1 − ρ² gives. The difference almost stays in
place (1.04 minutes), while the standard error becomes
0.235 and the p-value is much smaller. Since the number of users
needed is proportional to the variance, a test with CUPED gives the same
power with about 44% of the users.

## By simulation: power rises, false alarms do not

Let us not decide from one experiment. Let us compare the two methods on
300 real experiments (3% effect) and 300 A/A experiments:

```python
power = np.zeros(2)
alarm = np.zeros(2)
for s in range(300):
    for lift, counter in [(0.03, power), (0.0, alarm)]:
        t = make_engagement_test(seed=2000 + s, lift=lift)
        b = (t["group"] == "B").to_numpy()
        y = t["minutes"].to_numpy()
        x = t["pre_minutes"].to_numpy()
        counter += [compare(y, b)[2] < 0.05, compare(cuped(y, x), b)[2] < 0.05]
print(np.round(power / 300, 3), np.round(alarm / 300, 3))
```

```text
[0.613 0.92 ] [0.05 0.06]
```

The plain comparison has power 61.3%, CUPED 92.0%. On
the A/A experiments both methods give about 5% false alarms
(5.0% and 6.0%). CUPED is not a cheating shortcut: it
reduces the noise without breaking the test's validity.

## The trap: a covariate measured during the experiment

The only condition for the adjustment not changing the difference is that
X **is not affected by B**. Let us apply the same formula with the number
of sessions during the test (`sessions`). Sessions rise with minutes, so B
raises them too:

```python
sessions = test["sessions"].to_numpy()
print(compare(cuped(minutes, sessions), is_b))
```

```text
(0.403, 0.184, 0.0286)
```

The difference drops to 0.40 minutes: about half of the true
effect (0.82 minutes) has disappeared. The adjustment threw
away the effect B made through more sessions as a "session difference".
**The covariate is measured before the experiment;** nothing measured
during the test is used.

## Summary

- CUPED adjusts each user's metric with the value before the experiment
  (X): Y − θ(X − X̄).
- The remaining variance is about 1 − ρ²; with a high ρ the gain is large.
- The estimate of the effect does not change, the standard error shrinks,
  power rises, false alarms stay at 5%.
- X must be measured before assignment; a variable affected by the test
  can erase the effect.
