## Four steps

1. The primary metric's mean and deviation in past data.
2. The smallest worthwhile effect: relative (5%) or absolute (0.5 points).
3. n per group: `TTestIndPower().solve_power(effect_size=d, power=0.8,
   alpha=0.05)`; for rates `NormalIndPower` + `proportion_effectsize`.
4. Duration: $2n$ / (daily users × share entering the test), rounded up to
   full weeks.

## A quick estimate

```python
import math


def rule_of_16(sd, delta):
    return math.ceil(16 * sd**2 / delta**2)


print(rule_of_16(0.32, 0.006))
print(rule_of_16(0.32, 0.012))
```

```text
45512
11378
```

When the difference doubles, the people needed drop to a quarter.

## Checklist

- Is the unit counted the user? Do not calculate with visits.
- Do the base rate and deviation come **from past data**?
- Is the MDE smaller than the effect the team hopes for?
- With an unequal split, is `ratio` in the calculation?
- Is the duration at least one full week?
- Is another experiment running on the same traffic?
