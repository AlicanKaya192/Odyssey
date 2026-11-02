# The Peeking Trap and Sequential Testing

The test will run for two weeks, but the results dashboard updates every
day. On the third day p drops to 0.04; saying "it's significant, let's stop"
is very tempting. This section measures why this habit blows up the false
alarm rate and shows the right way to stop a test early: **sequential
testing**.

## A p-value every day

A function that, at the end of each day of a two-week test, runs a
two-proportion z-test on the users collected so far:

```python
import numpy as np
from scipy import stats
from ab_data import make_experiment


def daily_p(test, days=14):
    is_b = (test["group"] == "B").to_numpy()
    day = test["day"].to_numpy()
    bought = test["bought"].to_numpy().astype(float)
    size = days + 1
    n_a = np.cumsum(np.bincount(day[~is_b], minlength=size))[1:]
    n_b = np.cumsum(np.bincount(day[is_b], minlength=size))[1:]
    k_a = np.cumsum(np.bincount(day[~is_b], bought[~is_b], size))[1:]
    k_b = np.cumsum(np.bincount(day[is_b], bought[is_b], size))[1:]
    pooled = (k_a + k_b) / (n_a + n_b)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (k_b / n_b - k_a / n_a) / se
    return 2 * stats.norm.sf(np.abs(z))


def simulate(reps, lift, first_seed):
    seeds = range(first_seed, first_seed + reps)
    return np.array([daily_p(make_experiment(n=14000, seed=s, lift=lift))
                     for s in seeds])
```

`np.bincount` gives each day's user and purchase counts, `np.cumsum` the
totals so far; z is the pooled z-test from the Comparing Proportions
section. `simulate` repeats the same experiment with different seeds and
puts each experiment's 14 daily p-values in a row.

## Looking every day when there is no difference

500 A/A experiments (B has no effect at all). Depending on how often we
look, what is the probability of seeing p < 0.05 at least once?

```python
aa = simulate(500, 0.0, 1000)
for looks in [[14], [7, 14], list(range(2, 15, 2)), list(range(1, 15))]:
    hit = (aa[:, np.array(looks) - 1] < 0.05).any(axis=1)
    print(len(looks), round(float(hit.mean()), 3))
```

```text
1 0.046
2 0.08
7 0.172
14 0.228
```

- Looking only on the last day, the false alarm rate is 4.6%: the
  promised 5%.
- Looking twice makes it 8.0%, looking every day 22.8%.
  A change with no effect is declared a "win" in about one test in four by
  a team that looks every day.

Why? The p-value wanders randomly as data arrives. Each look gives it a new
chance to drop below the threshold, and the rule "stop when significant"
adds those chances up. It is the problem of the Multiple Comparisons
section in time: running the same test again and again.

## The fix: planning the looks in advance

If we want to stop early, we use a **stricter** threshold at each look, so
that the total false alarm rate over all looks stays at 5%. Two ways:

- **Bonferroni:** divide α by the number of looks: 0.05 / 14. Simple but
  too cautious.
- **A calibrated threshold:** in A/A simulations, look at the distribution
  of "the smallest p over 14 looks" and make its 5% point the threshold.
  Then the total false alarm rate lands right at 5%. (This is the method
  called the **Pocock** boundary, found by simulation.)

Let's find the threshold from one simulation and test it on **500 new A/A
experiments with other seeds**:

```python
bonferroni = 0.05 / 14
calibrated = np.quantile(aa.min(axis=1), 0.05)
print(round(bonferroni, 4), round(float(calibrated), 4))
fresh = simulate(500, 0.0, 5000)
for limit in [0.05, bonferroni, calibrated]:
    print(round(float((fresh.min(axis=1) < limit).mean()), 3))
```

```text
0.0036 0.0074
0.212
0.016
0.04
```

- Looking every day at 0.05 gives 21.2% false alarms on the new
  experiments too.
- Bonferroni 1.6%: safe but stricter than needed; the looks
  are not independent (the same data accumulates), so Bonferroni overpays.
- The calibrated threshold (0.0074) keeps false alarms at
  4.0%: close to 5%.

## The cost: power

The right to stop early is not free. With a real effect (B raises buying by
12%), let's compare the three ways:

```python
real = simulate(500, 0.12, 9000)
print(round(float((real[:, -1] < 0.05).mean()), 3))
for limit in [bonferroni, calibrated]:
    hit = real < limit
    stopped = hit.any(axis=1)
    first_day = hit.argmax(axis=1)[stopped] + 1
    print(round(float(stopped.mean()), 3), round(float(first_day.mean()), 1))
```

```text
0.736
0.5 8.4
0.584 7.7
```

- The fixed test that looks only on day 14 catches the effect
  73.6% of the time.
- The tests looking every day with a strict threshold catch the effect less
  often (50.0% and 58.4%), but when they do, with the
  calibrated threshold they stop after 7.7 days on average.

So sequential testing is a trade: an earlier decision in exchange for some
power over the same duration. Real sequential designs (e.g. **O'Brien–
Fleming** boundaries) shrink this loss by using thresholds that are very
strict at first and close to 0.05 at the end; for daily dashboards
"always-valid" p-values are also used. What they all share: **the rules are
written before the test starts.**

## In practice

- A fixed-duration test: the duration is in the plan, p is read only at
  the end.
- Watching guardrail metrics on the dashboard is fine: stopping because
  something **breaks** (cutting losses) does not create the false alarm
  problem, since no win is declared.
- If an early "win" is wanted, a sequential design is chosen at the start
  and its thresholds are written into the plan.
- As we saw in An Introduction to the Bayesian View section, with the
  Bayesian method too, wrong decisions become more frequent if the stopping
  rule is not written in advance.

## Summary

- Each look gives p a new chance to drop below the threshold; looking every
  day raised false alarms from 5% to 22.8%.
- Stopping early needs a stricter threshold at each look: Bonferroni is too
  cautious, a threshold calibrated by simulation hits 5%.
- The price of the right to stop early is power over the same duration.
- The rules are written before the test; stopping for guardrails is fine.
