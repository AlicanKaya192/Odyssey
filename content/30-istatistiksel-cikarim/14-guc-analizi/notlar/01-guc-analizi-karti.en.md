| Question | Class | Call |
|---|---|---|
| Two means, how many people? | `TTestIndPower` | `solve_power(effect_size=d, power=0.8, alpha=0.05)` |
| Two rates, how many people? | `NormalIndPower` | `solve_power(effect_size=h, power=0.8, alpha=0.05)` |
| Turn rates into h | — | `proportion_effectsize(p_b, p_a)` |
| Power with this n? | both | `power(effect_size=..., nobs1=n, alpha=0.05)` |
| MDE with this n? | both | `solve_power(nobs1=n, power=0.8, alpha=0.05)` |

`nobs1` is the size of the first group; by default the second group is the
same (`ratio=1`). The result is always rounded **up**.

## Power, α and one direction

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower

solver = TTestIndPower()
settings = [(0.05, 0.8, "two-sided"), (0.05, 0.9, "two-sided"),
            (0.01, 0.8, "two-sided"), (0.05, 0.8, "larger")]
for alpha, power, side in settings:
    n = solver.solve_power(effect_size=0.2, power=power, alpha=alpha,
                           alternative=side)
    print(alpha, power, side, int(np.ceil(n)))
```

```text
0.05 0.8 two-sided 394
0.05 0.9 two-sided 527
0.01 0.8 two-sided 586
0.05 0.8 larger 310
```

- Raising power from 0.8 to 0.9 or lowering α to 0.01 needs more people.
- A one-sided test needs fewer people; but the direction must be chosen
  **before** the test.

## Things to remember

- n is inversely proportional to the square of the effect: halve the effect
  and n quadruples.
- As the effect size, write not the effect you "hope for" but the smallest
  effect you do not want to miss.
- If the calculation looks doubtful, check it by simulation: thousands of
  tests of the same size, the share that come out significant.
