## Steps

1. Write the question and $H_0$ / $H_1$.
2. Choose the direction (two- or one-sided) and $\alpha$ before looking at
   the data.
3. Compute the test statistic and the p-value.
4. If $p < \alpha$, reject $H_0$; otherwise say "not rejected".
5. Report the effect and the confidence interval too.

## Terms

| Term | Meaning |
|---|---|
| Null hypothesis ($H_0$) | "No difference / no effect" |
| Alternative hypothesis ($H_1$) | "There is a difference" |
| Test statistic | The difference measured in standard errors |
| p-value | The probability of a result at least this extreme if $H_0$ is true |
| Significance level ($\alpha$) | The threshold chosen in advance |
| Type I error | A false alarm; probability $\alpha$ |
| Type II error | A miss; probability $\beta$ |
| Power | $1 - \beta$ |

## The one-sample t-test

```python
from scipy import stats

loads = [910, 860, 845, 930, 880, 905, 870, 925]
two = stats.ttest_1samp(loads, 850)
one = stats.ttest_1samp(loads, 850, alternative="greater")
print(round(two.statistic, 3), round(two.pvalue, 4), round(one.pvalue, 4))
```

```text
3.667 0.008 0.004
```

- `alternative`: `"two-sided"` (the default), `"greater"`, `"less"`.
- The one-sided p is half the two-sided one when the result goes in the
  expected direction.

## Decision table

| | $H_0$ true | $H_0$ false |
|---|---|---|
| Reject | type I error ($\alpha$) | correct (power) |
| Do not reject | correct | type II error ($\beta$) |
