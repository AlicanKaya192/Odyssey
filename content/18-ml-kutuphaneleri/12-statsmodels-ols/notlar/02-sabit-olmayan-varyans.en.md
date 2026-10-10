OLS standard errors rest on an assumption: the size of the error is the same
in every row. For house prices this often fails: the price of a 50 m² house
may be off by a few thousand, that of a 400 m² house by hundreds of
thousands. When the assumption breaks, the coefficient is still right but
**the confidence interval lies**.

```python
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan


def sample(seed):
    rng = np.random.default_rng(seed)
    area = rng.lognormal(4.3, 0.5, 200)                  # mostly small houses
    noise = rng.normal(0, 1, 200) * area ** 1.5 * 0.05   # big house, big error
    return sm.add_constant(area), 50 + 3 * area + noise


X, y = sample(3)
plain = sm.OLS(y, X).fit()
robust = sm.OLS(y, X).fit(cov_type="HC3")
print(round(het_breuschpagan(plain.resid, X)[1], 4))
print(round(plain.bse[1], 3), round(robust.bse[1], 3))
hits = {"plain": 0, "HC3": 0}
for seed in range(100, 600):
    X, y = sample(seed)
    for name, kind in [("plain", "nonrobust"), ("HC3", "HC3")]:
        low, high = sm.OLS(y, X).fit(cov_type=kind).conf_int()[1]
        hits[name] += bool(low <= 3 <= high)
print({k: v / 500 for k, v in hits.items()})
```

```text
0.0
0.085 0.309
{'plain': 0.578, 'HC3': 0.934}
```

## What we see

- The Breusch–Pagan test's p-value is 0: the error variance is not
  constant.
- The standard error of the area coefficient is 0.085 by the classic
  formula and 0.309 by the robust one (`HC3`): the real uncertainty is
  nearly four times larger.
- We repeated the experiment 500 times and counted how often the 95%
  confidence interval contained the true coefficient (3). The classic
  interval caught it only 57.8% of the time; saying "95% sure", it is wrong
  almost half the time. The HC3 interval 93.4%, close to its claim.

## When

- If the residuals grow with the fitted value (a funnel shape) or
  Breusch–Pagan gives a small p, use `cov_type="HC3"`.
- The coefficients do not change; only the standard error, p-value and
  interval do.
- If the variance is constant, HC3 comes out close to the classic one; the
  cost of using it when in doubt is small.
