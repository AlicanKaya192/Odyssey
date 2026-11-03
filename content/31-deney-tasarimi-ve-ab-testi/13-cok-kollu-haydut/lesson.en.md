# Multi-Armed Bandits

A classic A/B test splits the traffic equally from start to finish: an
option that turns out to be bad still gets a third (or half) of the users
until the test ends. This section covers methods that **shift the traffic
towards the option that looks good** while the test runs. The name comes
from casino machines: each option is a machine with its own arm, and the
goal is to win the most in total. The gain is real, but it has a price:
measuring becomes harder.

## Explore or exploit?

We have three headline options; their buying rates are truly 5%, 5.5% and
6.5% (we know, the algorithm does not). 30,000 visitors will come. Two
ways:

- **A fixed split:** send everyone at random, equally, to the three arms (a
  classic A/B/C test).
- **Thompson sampling:** keep the Beta distribution from the An
  Introduction to the Bayesian View section for each arm's rate; for every
  visitor draw one value from each arm and show the largest. Uncertain arms
  win now and then (exploration), the arm that looks good wins most of the
  time (exploitation).

In practice the algorithm is updated in batches, not after every visitor;
here every 500 visitors:

```python
import numpy as np

RATES = np.array([0.050, 0.055, 0.065])
VISITORS, BATCH = 30000, 500


def fixed_split(seed):
    rng = np.random.default_rng(seed)
    arm = rng.integers(0, 3, VISITORS)
    bought = rng.random(VISITORS) < RATES[arm]
    return np.bincount(arm, minlength=3), np.bincount(arm, bought, 3)


def thompson(seed):
    rng = np.random.default_rng(seed)
    n = np.zeros(3)
    k = np.zeros(3)
    for _ in range(VISITORS // BATCH):
        draws = rng.beta(1 + k, 1 + n - k, (BATCH, 3))
        arm = draws.argmax(axis=1)
        bought = rng.random(BATCH) < RATES[arm]
        n += np.bincount(arm, minlength=3)
        k += np.bincount(arm, bought, 3)
    return n, k


for name, method in [("fixed", fixed_split), ("thompson", thompson)]:
    n, k = method(1)
    print(name, n.astype(int).tolist(), int(k.sum()))
```

```text
fixed [10042, 9990, 9968] 1714
thompson [402, 1566, 28032] 1909
```

The fixed split sends about 10,000 people to each arm. Thompson sampling
soon sees that the third arm is good and directs most visitors to it; only
402 people go to the worst arm. Sales are 1,909 instead of
1,714.

## Regret: lost sales

One run can mislead. Let us run both methods 200 times. **Regret** is the
difference between the sales expected if everyone had been sent to the best
arm from the start and the sales that happened:

```python
best = RATES.max() * VISITORS
for name, method in [("fixed", fixed_split), ("thompson", thompson)]:
    sales, right = [], 0
    for s in range(200):
        n, k = method(100 + s)
        sales.append(k.sum())
        right += (k / np.maximum(n, 1)).argmax() == 2
    print(name, round(float(np.mean(sales))), round(best - np.mean(sales)),
          right / 200)
```

```text
fixed 1698 252 1.0
thompson 1892 58 1.0
```

The fixed split loses 252 sales on average, Thompson sampling
58. Both find the best arm correctly in the end
(100%). The bandit shrinks the **cost** of the test.

## The price: measurement breaks

Since the bandit sends few users to the arm that looks bad, that arm's
estimate is both noisy and **biased**: an arm that gets an unlucky start is
rarely chosen again, and its low estimate cannot be corrected. The average
estimates over 200 runs:

```python
est_fixed, est_ts = [], []
for s in range(200):
    n, k = fixed_split(100 + s)
    est_fixed.append(k / n)
    n, k = thompson(100 + s)
    est_ts.append(k / np.maximum(n, 1))
print(np.round(np.mean(est_fixed, axis=0), 4))
print(np.round(np.mean(est_ts, axis=0), 4))
```

```text
[0.05   0.0551 0.0647]
[0.0457 0.0526 0.0648]
```

The fixed split's estimates sit on the true rates (0.05, 0.055 and 0.065).
Thompson sampling estimates the worst arm's rate as 4.57% on
average: below the truth. That is why computing an ordinary z-test or
confidence interval on the bandit's data misleads; the condition from the
Random Assignment section, "every user has the same chance of each group",
no longer holds.

## When a bandit, when an A/B test?

| Situation | Suitable |
|---|---|
| A short-lived decision (a campaign headline, a weekly recommendation) | bandit |
| Every lost conversion is expensive, learning is secondary | bandit |
| A lasting product decision, the size of the effect will be reported | A/B test |
| Guardrail metrics and the long-term effect matter | A/B test |
| Many options that keep changing | bandit |

A bandit answers "which one is best?" quickly; it does not reliably answer
"how much better?".

## Summary

- A multi-armed bandit shifts traffic towards the option that looks good
  while the test runs.
- Thompson sampling draws a value from each arm's Beta distribution and
  picks the largest: exploration and exploitation are balanced.
- Regret is the sales lost compared with the best arm; a bandit shrinks it
  greatly.
- The price: rarely chosen arms get noisy and biased estimates; classic
  tests cannot be applied directly.
