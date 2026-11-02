## Formulas

| What | Formula |
|---|---|
| Between-group sum of squares | $\sum_g n_g (\bar{x}_g - \bar{x})^2$ |
| Within-group sum of squares | $\sum_g \sum_i (x_{gi} - \bar{x}_g)^2$ |
| F | $\dfrac{SS_{between} / (k-1)}{SS_{within} / (N-k)}$ |
| Effect size | $\eta^2 = SS_{between} / (SS_{between} + SS_{within})$ |

## In code

```python
from scipy import stats
from statsmodels.stats.oneway import anova_oneway
from ab_data import make_layout_test

test = make_layout_test()
groups = [g["minutes"] for _, g in test.groupby("layout")]
classic = stats.f_oneway(*groups)
welch = anova_oneway(test["minutes"], test["layout"], use_var="unequal")
print(round(classic.statistic, 3), f"{classic.pvalue:.1e}")
print(round(welch.statistic, 3), f"{welch.pvalue:.1e}")
```

```text
7.692 4.8e-05
7.314 9.2e-05
```

- `stats.f_oneway`: classical ANOVA, assumes equal variances.
- `anova_oneway(..., use_var="unequal")`: Welch's ANOVA; for when the
  deviations differ. Here the deviations are close, so the two results are
  similar.
- `stats.tukey_hsd(*groups)`: which pairs differ; `.statistic` holds the mean
  differences, `.pvalue` the adjusted p-values.

## Flow

1. Look at the groups' means and deviations.
2. ANOVA (Welch if the deviations differ a lot).
3. If p is small, look at the pairs with Tukey HSD.
4. Report: the group means, F, p, $\eta^2$ and the pairs that differ.

## How many pairs?

For $k$ groups there are $k(k-1)/2$ pairs: 6 for 4 groups, 15 for 6, 45 for
10.
