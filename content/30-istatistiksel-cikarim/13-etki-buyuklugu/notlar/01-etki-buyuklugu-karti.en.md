| Metric type | Effect size | Formula |
|---|---|---|
| Mean | Cohen's d | $(\bar{x}_B - \bar{x}_A) / s_p$ |
| Rate | Risk difference | $p_B - p_A$ |
| Rate | Relative risk | $p_B / p_A$ |
| Rate | Odds ratio | $\frac{p_B / (1 - p_B)}{p_A / (1 - p_A)}$ |
| Rate | Cohen's h | $2\arcsin\sqrt{p_B} - 2\arcsin\sqrt{p_A}$ |
| Two groups, ranks | Common language | $U / (n_A n_B)$ |
| Many groups | η² (eta squared) | between-group squares / total squares |
| Cross table | Cramér's V | `stats.contingency.association` |

Rough guide (d and h): 0.2 small, 0.5 medium, 0.8 large. Domain knowledge
always comes first.

## All together

```python
import numpy as np


def rate_effects(p_a, p_b):
    odds_a, odds_b = p_a / (1 - p_a), p_b / (1 - p_b)
    h = 2 * np.arcsin(np.sqrt(p_b)) - 2 * np.arcsin(np.sqrt(p_a))
    return [round(p_b - p_a, 3), round(p_b / p_a, 2),
            round(odds_b / odds_a, 2), round(float(h), 3)]


print(rate_effects(0.10, 0.12))
print(rate_effects(0.50, 0.60))
```

```text
[0.02, 1.2, 1.23, 0.064]
[0.1, 1.2, 1.5, 0.201]
```

- The relative risk is similar on both lines, but the risk difference and h
  are very different.
- As the base rate rises, the odds ratio moves away from the relative risk.

## Reporting order

1. The two groups' values (means or rates), the ns.
2. The difference and its confidence interval, in the metric's own unit.
3. A standard effect size (d, h) if needed.
4. The p-value.
5. The comparison with a practical threshold set in advance.
