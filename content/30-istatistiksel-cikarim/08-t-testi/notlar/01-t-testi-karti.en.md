## Which t-test?

| Data | Test | Code |
|---|---|---|
| One group, against a known value | one-sample | `stats.ttest_1samp(x, mu0)` |
| Two separate groups | Welch | `stats.ttest_ind(b, a, equal_var=False)` |
| The same units, two measurements | paired | `stats.ttest_rel(before, after)` |

## The result object

```python
from scipy import stats

a = [8.1, 6.5, 9.9, 7.2, 5.8, 8.8, 7.7, 6.9]
b = [9.4, 8.2, 11.0, 7.9, 9.1, 10.3, 8.6, 9.8]
result = stats.ttest_ind(b, a, equal_var=False)
low, high = result.confidence_interval(0.95)
print(round(result.statistic, 3), round(result.pvalue, 4))
print(round(result.df, 1))
print(round(low, 2), round(high, 2))
```

```text
2.807 0.0145
13.4
0.39 2.96
```

- `statistic`: t; `pvalue`: p; `df`: the degrees of freedom (can be
  fractional with Welch).
- `confidence_interval(0.95)`: the interval of the difference first group
  minus second group. The order matters: `ttest_ind(b, a)` means "b − a".

## Formulas

- Welch: $t = \dfrac{\bar{x}_B - \bar{x}_A}{\sqrt{s_A^2/n_A + s_B^2/n_B}}$
- Paired: using the differences $d_i$, $t = \dfrac{\bar{d}}{s_d/\sqrt{n}}$

## Three questions when choosing

1. Are the groups made of the same units? Yes → paired.
2. Could the deviations and group sizes differ? Always say "they could" →
   Welch.
3. Is the sample small and the data very skewed? Yes → a non-parametric test
   or the bootstrap.
