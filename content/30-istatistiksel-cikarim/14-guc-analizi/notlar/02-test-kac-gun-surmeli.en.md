Power analysis gives the number of people per group. The real question is
often "how many days will this test take?".

## From people to days

The total number of people (both groups) is divided by the daily visitors:

```python
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def days_needed(p_a, p_b, daily_visitors):
    h = proportion_effectsize(p_b, p_a)
    n = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
    return int(np.ceil(2 * np.ceil(n) / daily_visitors))


print(days_needed(0.114, 0.130, 1500))
print(days_needed(0.114, 0.122, 1500))
```

```text
9
35
```

Catching a difference half as large (from 11.4% to 12.2%) takes about four
times as long. If the duration is unacceptable there are three ways out:
aim for a larger effect, give the test more traffic, or choose a less noisy
metric.

## When setting the duration

- **At least one full week.** Users behave differently on weekdays and
  weekends; a three-day test represents only part of the week.
- **The duration is written in advance.** "We stop when it becomes
  significant" inflates the false alarm rate; we will see this in the
  experiment design module.
- **The base rate comes from past data**, not a guess. A wrong base rate
  shifts the whole calculation.
- **Not all traffic may enter the test.** If only visitors to the checkout
  page count, the daily visitors are that page's.
