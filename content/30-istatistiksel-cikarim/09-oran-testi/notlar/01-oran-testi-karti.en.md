## Formulas

| What | Formula |
|---|---|
| Proportion | $\hat{p} = k / n$ |
| Common proportion (under $H_0$) | $\hat{p} = (k_A + k_B) / (n_A + n_B)$ |
| Standard error of the difference | $\sqrt{\hat{p}(1-\hat{p})(1/n_A + 1/n_B)}$ |
| Test statistic | $z = (\hat{p}_B - \hat{p}_A) / SE$ |
| Relative lift | $(\hat{p}_B - \hat{p}_A) / \hat{p}_A$ |

## In code

```python
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.proportion import confint_proportions_2indep

k_b, n_b, k_a, n_a = 130, 1000, 105, 1000
z, p = proportions_ztest([k_b, k_a], [n_b, n_a])
low, high = confint_proportions_2indep(k_b, n_b, k_a, n_a, method="newcomb")
fisher = stats.fisher_exact([[k_b, n_b - k_b], [k_a, n_a - k_a]])
print(round(z, 3), round(p, 4), round(fisher.pvalue, 4))
print(round(low, 4), round(high, 4))
```

```text
1.736 0.0826 0.0954
-0.0033 0.0533
```

- `proportions_ztest(counts, sample sizes)`: the order is "first minus
  second".
- `confint_proportions_2indep(k1, n1, k2, n2)`: the interval of the
  difference `k1/n1 − k2/n2`.
- `fisher_exact` needs a 2×2 table: each row a group, the columns
  `[yes, no]`.
- In a test with thousands of users the z and Fisher p-values come out
  close.

## Which test?

| Situation | Test |
|---|---|
| Large groups | the z-test |
| An expected count < 5 in any cell | Fisher |
| More than two groups | chi-square (the next section) |
