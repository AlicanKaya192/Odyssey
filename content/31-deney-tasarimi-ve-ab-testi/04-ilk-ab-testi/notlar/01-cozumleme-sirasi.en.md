| Step | Question | If it fails |
|---|---|---|
| 1. SRM | Do the group sizes match the design? | Stop, find the cause |
| 2. Balance | Are earlier traits equal? | Inspect the assignment |
| 3. Duration | Did it run as planned, full weeks? | Early-look warning |
| 4. Primary metric | Difference, interval, p | — |
| 5. Secondary metrics | Why is it so? | Careful in interpretation |
| 6. Guardrail metrics | Did something break? | Stop |
| 7. Decision | By the rule in the plan | — |

## The primary metric in one function

```python
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportions_ztest)


def primary(k_a, n_a, k_b, n_b):
    p = proportions_ztest([k_b, k_a], [n_b, n_a])[1]
    low, high = confint_proportions_2indep(k_b, n_b, k_a, n_a)
    return [round(k_b / n_b - k_a / n_a, 4), round(float(low), 4),
            round(float(high), 4), round(float(p), 4)]


print(primary(1766, 15041, 1940, 14959))
```

```text
[0.0123, 0.0048, 0.0197, 0.0012]
```

Order: the difference, the lower and upper ends of the interval, p.

## The decision table

| Interval | Decision |
|---|---|
| Lower end above the practical threshold | ship |
| Above zero but reaching below the threshold | unclear: by cost or more data |
| Contains zero | no evidence |
| Entirely below zero | roll back, investigate |
