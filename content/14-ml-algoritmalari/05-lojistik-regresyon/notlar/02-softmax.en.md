With more than two classes, each class has its own weight vector and
**softmax** is used instead of the sigmoid: `pₖ = e^(zₖ) / Σⱼ e^(zⱼ)`. All
probabilities are positive and add up to 1. The gradient has the same simple
form: `Aᵀ (P − Y) / n`; here `Y` is the **one-hot** matrix with a 1 at the
position of the right class in each row.

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(7)
centers = np.array([[0, 0], [3, 0], [0, 3]])
y = rng.integers(0, 3, 240)
X = centers[y] + rng.normal(0, 1.2, size=(240, 2))
A = np.column_stack([np.ones(240), X])
Y = np.eye(3)[y]


def softmax(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(axis=1, keepdims=True)


W = np.zeros((3, 3))
for _ in range(5000):
    P = softmax(A @ W)
    W -= 0.5 * A.T @ (P - Y) / len(y)
P = softmax(A @ W)
ref = LogisticRegression(C=np.inf, max_iter=1000).fit(X, y)
print(round((P.argmax(axis=1) == y).mean(), 3))
print((P.argmax(axis=1) == ref.predict(X)).mean())
print(np.abs(P - ref.predict_proba(X)).max().round(4))
print(P[0].round(3), P[0].sum().round(6))
```

```text
0.908
1.0
0.0002
[0.015 0.002 0.983] 1.0
```

With three classes the accuracy is 0.908; all predictions match
scikit-learn's and the probabilities differ by at most 0.0002. In softmax,
subtracting the largest `z` (`Z - Z.max(...)`) does not change the result but
keeps `e^z` from overflowing.

We compared probabilities, not weights: in softmax, adding the same vector to
all classes' weights does not change the probabilities, so without
regularisation the weights are not unique.
