## One group's ratio and standard error

```python
import numpy as np


def ratio_and_se(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    r = y.mean() / x.mean()
    var = (y.var(ddof=1) - 2 * r * np.cov(x, y)[0, 1]
           + r ** 2 * x.var(ddof=1)) / (len(x) * x.mean() ** 2)
    return round(float(r), 4), round(float(np.sqrt(var)), 4)


views = [1, 2, 10, 40, 3]
clicks = [1, 1, 2, 4, 0]
print(ratio_and_se(views, clicks))
print(round(float(np.mean(np.array(clicks) / np.array(views))), 4))
```

```text
(0.1429, 0.0433)
0.36
```

The first line is the ratio of totals and the delta standard error, the
second the mean of user rates. The same data, two very different "rates":
the user with 40 views weighs heavily in the first, while in the second
every user gets one vote.

## The difference of two groups

- Difference: R_B − R_A.
- Standard error: √(var_A + var_B) (the groups are independent).
- z = difference / standard error, p = 2 · (1 − Φ(|z|)).

## The parts of the formula

| Symbol | Meaning |
|---|---|
| n | number of users (not views) |
| X̄, Ȳ | average views and clicks per user |
| s_X², s_Y² | user-level variances |
| s_XY | user-level covariance |
| R | Ȳ / X̄ |
