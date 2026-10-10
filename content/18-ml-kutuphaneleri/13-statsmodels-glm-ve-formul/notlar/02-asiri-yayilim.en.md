The Poisson model makes a strong assumption: a count's variance **equals** its
mean. In real data people differ from one another (one never comes, another
comes every week) and the variance is often larger than the mean. This is
called **overdispersion**. The coefficient still lands near the right place,
but the standard errors stay too small.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def sample(seed):
    rng = np.random.default_rng(seed)
    risk = rng.normal(0, 1, 500)
    mood = rng.gamma(1.0, 1.0, 500)          # a personal, unmeasured difference
    visits = rng.poisson(np.exp(1 + 0.3 * risk) * mood)
    return pd.DataFrame({"visits": visits, "risk": risk})


df = sample(5)
print(round(df.visits.mean(), 2), round(df.visits.var(), 2))
pois = smf.glm("visits ~ risk", data=df, family=sm.families.Poisson()).fit()
print(round(pois.pearson_chi2 / pois.df_resid, 2))
families = {"poisson": sm.families.Poisson(),
            "negbin": sm.families.NegativeBinomial(alpha=1.0)}
hits = {name: 0 for name in families}
for seed in range(1000, 1200):
    data = sample(seed)
    for name, family in families.items():
        fit = smf.glm("visits ~ risk", data=data, family=family).fit()
        low, high = fit.conf_int().loc["risk"]
        hits[name] += bool(low <= 0.3 <= high)
print({k: v / 200 for k, v in hits.items()})
```

```text
2.72 10.62
3.66
{'poisson': 0.685, 'negbin': 0.945}
```

## What we see

- Mean 2.72, variance 10.62: Poisson's "the two are equal" assumption is
  clearly broken.
- The ratio of the Pearson chi-square to its degrees of freedom is 3.66. For
  data that fits Poisson this number is close to 1; above 1.5 is a sign of
  overdispersion.
- Over 200 repeats the Poisson 95% interval contained the true coefficient
  (0.3) only 68.5% of the time. The negative binomial (a count model whose
  variance may exceed its mean) 94.5%, close to its claim.

## When

- If the variance of count data is clearly larger than its mean, or the
  Pearson ratio exceeds 1.5, use the negative binomial.
- The `alpha` in `NegativeBinomial(alpha=...)` is the amount of spread;
  `smf.negativebinomial(...)` estimates it from the data itself.
- If only predictions are wanted, Poisson may still do; the problem is in
  the uncertainty.
