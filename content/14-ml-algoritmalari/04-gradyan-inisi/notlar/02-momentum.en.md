In a narrow valley gradient descent zigzags between the walls and moves slowly
towards the bottom. **Momentum** accumulates the gradients:
`v ← β v + ∇L`, `w ← w − η v`. Gradients pointing the same way reinforce each
other, the two sides of the zigzag cancel out.

```python
import numpy as np

rng = np.random.default_rng(6)
n = 200
X = np.column_stack([rng.uniform(0, 1, n), rng.uniform(0, 10, n)])
y = 1 + 2 * X[:, 0] + 0.5 * X[:, 1] + rng.normal(0, 0.1, n)
A = np.column_stack([np.ones(n), X])
target = ((A @ np.linalg.lstsq(A, y, rcond=None)[0] - y) ** 2).mean()


def steps(lr, beta):
    w, v = np.zeros(3), np.zeros(3)
    for step in range(1, 200_001):
        v = beta * v + 2 / n * A.T @ (A @ w - y)    # beta = 0: plain descent
        w -= lr * v
        if ((A @ w - y) ** 2).mean() <= target * 1.01:
            return step
    return None


for lr in (0.001, 0.01):
    print(lr, steps(lr, 0.0), steps(lr, 0.9))
```

```text
0.001 25762 2554
0.01 2575 233
```

With the same learning rate, momentum (`β = 0.9`) reached the target in about
ten times fewer steps. **Adam**, used in neural networks, in addition to
momentum adjusts each weight's step size by its own gradient history; it is
even more robust to differences in scale.
