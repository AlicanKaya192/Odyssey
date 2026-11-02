## A bootstrap interval for two groups

```python
import numpy as np


def boot_ci(a, b, stat, reps=2000, seed=0):
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a), np.asarray(b)
    values = [stat(rng.choice(b, len(b))) - stat(rng.choice(a, len(a)))
              for _ in range(reps)]
    low, high = np.percentile(values, [2.5, 97.5])
    return round(float(low), 2), round(float(high), 2)


a = [12, 15, 9, 30, 14, 11, 13, 50, 10, 12]
b = [16, 18, 12, 35, 15, 17, 14, 60, 13, 16]
print(boot_ci(a, b, np.mean))
print(boot_ci(a, b, np.median))
```

```text
(-7.8, 15.3)
(-6.0, 12.5)
```

The mean, the median or any function can be given as `stat`.

## The permutation test

1. Compute the real difference.
2. Shuffle the group labels (`rng.permutation`) and compute the difference
   again.
3. Repeat thousands of times.
4. p = the share where |shuffled difference| ≥ |real difference|.

## When to use which?

| Situation | Tool |
|---|---|
| Large sample, mean or rate | a formula (Welch, z) |
| A statistic without a formula | bootstrap |
| A test without a distribution assumption | permutation |
| A small, very skewed sample | none is fully reliable; more data |

## Watch out

- Resampling is done **at the unit of assignment**: if users were assigned,
  users are resampled, not page views.
- The seed is fixed so the result can be reproduced.
- 2000 repeats are usually enough for an interval; more for a small p.
