Naive Bayes assumes the features are independent within a class. When
features carry the same information (a price and the price with tax, say), the
model counts that evidence several times. The extreme case: copying the same
feature.

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB

rng = np.random.default_rng(19)
y = rng.integers(0, 2, 400)
x = rng.normal(0, 1, 400) + 1.0 * y
Xt = np.array([[0.8]])
for copies in (1, 3, 10):
    # copies of the same feature
    X = np.repeat(x[:, None], copies, axis=1)
    p = GaussianNB().fit(X, y).predict_proba(np.repeat(Xt, copies, axis=1))[0, 1]
    print(copies, round(p, 3))
yt = rng.integers(0, 2, 2000)
xt = rng.normal(0, 1, 2000) + yt
for copies in (1, 10):
    X = np.repeat(x[:, None], copies, axis=1)
    m = GaussianNB().fit(X, y)
    p = m.predict_proba(np.repeat(xt[:, None], copies, axis=1))[:, 1]
    accuracy = ((p > 0.5) == yt).mean()
    # the probability's squared error
    brier = np.mean((p - yt) ** 2)
    print(copies, round(float(accuracy), 3), round(float(brier), 3))
```

```text
1 0.591
3 0.7
10 0.926
1 0.696 0.198
10 0.7 0.265
```

For the same sample, the probability of class 1 is 0.591 with one feature and
0.926 with ten copies: no new information, but the model is much surer. The
accuracy does not change (0.696 → 0.7), because the decision boundary is in the
same place; but the **Brier score** (the squared error of the probability),
which measures the quality of probabilities, gets worse from 0.198 to 0.265.
Naive Bayes is good at classifying, while its probabilities are often
overconfident; if probabilities are needed, they are calibrated afterwards or
features that are very similar to each other are weeded out.
