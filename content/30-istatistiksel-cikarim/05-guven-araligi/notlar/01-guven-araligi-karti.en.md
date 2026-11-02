## Formulas

| What | 95% confidence interval |
|---|---|
| Mean | $\bar{x} \pm t_{0.975;\,n-1} \cdot \dfrac{s}{\sqrt{n}}$ |
| Proportion (Wald) | $\hat{p} \pm 1.96\sqrt{\dfrac{\hat{p}(1-\hat{p})}{n}}$ |
| Proportion (Wilson) | `proportion_confint(..., method="wilson")` |

## In code

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

x = np.array([7.2, 3.2, 10.9, 5.5, 8.1, 6.4, 12.0, 4.8])
se = stats.sem(x)
low, high = stats.t.interval(0.95, df=len(x) - 1, loc=x.mean(), scale=se)
print(round(float(low), 2), round(float(high), 2))
low, high = proportion_confint(53, 400, alpha=0.05, method="wilson")
print(round(low, 4), round(high, 4))
```

```text
4.76 9.77
0.1027 0.1692
```

## Multipliers

| Confidence | Normal | t, 4 df | t, 99 df |
|---|---|---|---|
| 90% | 1.645 | 2.132 | 1.660 |
| 95% | 1.960 | 2.776 | 1.984 |
| 99% | 2.576 | 4.604 | 2.626 |

(df: degrees of freedom.) All are computed with
`stats.norm.ppf((1 + confidence) / 2)` and
`stats.t.ppf((1 + confidence) / 2, df)`.

## Choosing

- Mean: always the t multiplier (`stats.t.interval`).
- Proportion: Wilson; Wald only with large samples and when the proportion
  is not near 0 or 1.
- `alpha` is the share left outside: `alpha=0.05` → 95%.
