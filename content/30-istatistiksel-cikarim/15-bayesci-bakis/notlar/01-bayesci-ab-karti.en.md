| Concept | Meaning | Calculation |
|---|---|---|
| Prior | the belief before the data | Beta(a, b); flat prior Beta(1, 1) |
| Posterior | the belief after the data | Beta(a + k, b + n − k) |
| Credible interval | the rate is here with 95% probability | `stats.beta(...).ppf([0.025, 0.975])` |
| P(B > A) | the probability B is better | `(draw_b > draw_a).mean()` on the draws |
| Expected loss | the average cost of a wrong choice | `np.maximum(draw_a - draw_b, 0).mean()` |

## Bayesian A/B in one function

```python
import numpy as np


def bayes_ab(k_a, n_a, k_b, n_b, seed=0, draws=200_000):
    rng = np.random.default_rng(seed)
    draw_a = rng.beta(1 + k_a, 1 + n_a - k_a, draws)
    draw_b = rng.beta(1 + k_b, 1 + n_b - k_b, draws)
    prob_b = (draw_b > draw_a).mean()
    loss_b = np.maximum(draw_a - draw_b, 0).mean()
    return round(float(prob_b), 3), round(float(loss_b), 5)


print(bayes_ab(472, 4000, 560, 4000))
print(bayes_ab(3, 60, 7, 60))
```

```text
(0.998, 0.0)
(0.896, 0.0026)
```

- In the large test P(B > A) is close to one and the expected loss of
  choosing B is almost zero.
- In the small test B also looks ahead, but if we are wrong our loss is much
  larger.

## Watch out

- The prior is written **before** the data, with a justification.
- As the number of draws grows the results become stable; with a fixed seed
  they are the same on every run.
- The decision rule (e.g. "choose once the expected loss drops below 0.001")
  is written before the test.
