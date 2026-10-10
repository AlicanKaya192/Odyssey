In real questions the solution cannot take any value: rates stay between 0
and 1, shares add up to 1, a budget cannot be exceeded. `minimize` takes these
in two ways: **bounds** (`bounds`, a lower-upper limit for each variable) and
**constraints** (`constraints`, an equality or inequality between
variables).

An example: splitting money among three investments to make the risk
(variance) smallest.

```python
import numpy as np
from scipy import optimize

cov = np.array([[0.04, 0.006, 0.002],
                [0.006, 0.09, 0.01],
                [0.002, 0.01, 0.0225]])


def risk(w):
    return float(w @ cov @ w)


sum_to_one = {"type": "eq", "fun": lambda w: w.sum() - 1}
res = optimize.minimize(risk, x0=np.full(3, 1 / 3), bounds=[(0, 1)] * 3,
                        constraints=[sum_to_one])
print(res.success, res.x.round(3).tolist(), round(float(res.x.sum()), 6))
print(round(risk(np.full(3, 1 / 3)), 5), round(res.fun, 5))
free = optimize.minimize(risk, x0=np.full(3, 1 / 3))
print(float(np.abs(free.x).max()) < 1e-4)
```

```text
True [0.329, 0.076, 0.595] 1.0
0.02094 0.0148
True
```

## What happened?

- `bounds=[(0, 1)] * 3`: each share between 0 and 1 (no short selling).
- `{"type": "eq", "fun": ...}`: `fun` must be **zero**, that is, the shares
  add up to 1. For an inequality, `"type": "ineq"`: `fun` must be **zero or
  more**.
- The result: 59.5% to the least risky third investment, 7.6% to the riskiest
  second one. Compared with an equal split (0.02094) the risk fell to 0.0148.
- With the constraint removed, the solver found the answer "invest nothing":
  every share 0, risk 0. Mathematically right, meaningless. **Forgetting a
  constraint** is the most common mistake in optimisation: the solver solves
  what was written, not what was meant.

## The method

When constraints are given, `minimize` switches by itself to a method that
knows about constraints (SLSQP). The more clearly constraints and bounds are
written, the more reliable the solution; still check that the result really
satisfies the constraints (`res.x.sum()`).
