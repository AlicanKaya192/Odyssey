## Two tests

| Test | Question | scipy | Degrees of freedom |
|---|---|---|---|
| Goodness of fit | Do the counts fit the expected distribution? | `stats.chisquare(observed, f_exp=expected)` | categories − 1 |
| Independence | Are two categorical variables related? | `stats.chi2_contingency(table)` | (rows − 1)(columns − 1) |

## An unequal expectation

If the expected distribution is not even, pass `f_exp`. Its total must
equal the total of the observed counts:

```python
from scipy import stats

observed = [182, 174, 195, 172, 217, 216, 244]
shares = [0.13, 0.13, 0.13, 0.13, 0.14, 0.17, 0.17]
expected = [s * sum(observed) for s in shares]
result = stats.chisquare(observed, f_exp=expected)
print(round(result.statistic, 2), round(result.pvalue, 4))
```

```text
6.26 0.3942
```

With a model that expects more orders at the weekend, the same data is no
longer surprising: p is large.

## Formulas

- $\chi^2 = \sum (O - E)^2 / E$
- Expected under independence: row total × column total / grand total
- Cramér's V: `stats.contingency.association(table, method="cramer")`

## Checklist

- The table holds counts, not percentages.
- All expected counts are ≥ 5.
- On 2×2, `correction=False` gives the same result as the z-test; the
  default Yates correction is a little conservative.
