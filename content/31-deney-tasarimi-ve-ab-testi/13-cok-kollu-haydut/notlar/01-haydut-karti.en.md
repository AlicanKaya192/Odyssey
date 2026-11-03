## The probability that each arm is best

```python
import numpy as np

rng = np.random.default_rng(0)
k = np.array([12, 30, 25])
n = np.array([300, 500, 400])
draws = rng.beta(1 + k, 1 + n - k, (20000, 3))
best = draws.argmax(axis=1)
print([round(float((best == j).mean()), 3) for j in range(3)])
```

```text
[0.044, 0.413, 0.543]
```

Thompson sampling distributes the next visitor to the arms with exactly
these probabilities: the arm with a high probability of being best gets
more visitors.

## Three common methods

| Method | How it chooses | Note |
|---|---|---|
| ε-greedy (epsilon-greedy) | a random arm with probability ε, otherwise the best-looking | simple; ε is chosen by hand |
| UCB | the largest estimate + uncertainty margin | gives a margin to rarely tried arms |
| Thompson sampling | draw a value from each arm's distribution, the largest | few settings, good in practice |

## Glossary

- **Arm:** one option.
- **Exploration / exploitation:** trying a little-known arm / choosing the
  best-looking one.
- **Regret:** the gain lost compared with the best arm.
