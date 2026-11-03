## Three corrections in one function

```python
from statsmodels.stats.multitest import multipletests

p = [0.001, 0.012, 0.021, 0.038, 0.3]
for method in ["bonferroni", "holm", "fdr_bh"]:
    reject, p_adj = multipletests(p, alpha=0.05, method=method)[:2]
    print(method, *reject.astype(int), *[round(float(x), 4) for x in p_adj])
```

```text
bonferroni 1 0 0 0 0 0.005 0.06 0.105 0.19 1.0
holm 1 1 0 0 0 0.005 0.048 0.063 0.076 0.3
fdr_bh 1 1 1 1 0 0.005 0.03 0.035 0.0475 0.3
```

Each line first shows the decision for the five tests (1 = an accepted
finding), then the **adjusted p**-values. An adjusted p is compared
directly with 0.05: instead of changing the threshold it enlarges the p.

## By hand (m tests, α = 0.05)

| Method | Rule | What it protects |
|---|---|---|
| Bonferroni | p < α / m | the family-wise error rate (FWER) |
| Holm | k-th sorted p < α / (m − k + 1); stop at the first failure | FWER |
| Benjamini–Hochberg | all up to the largest k with k-th sorted p ≤ k · α / m | the false discovery rate (FDR) |

## Reminders

- m is the number of tests **looked at**; the ones seen on the dashboard
  and ignored count too.
- Holm never finds less than Bonferroni; both protect the same thing, so
  choosing Holm is free.
- BH's "5%" is the expected share of false ones among the findings; it is
  not the probability of a single false alarm.
