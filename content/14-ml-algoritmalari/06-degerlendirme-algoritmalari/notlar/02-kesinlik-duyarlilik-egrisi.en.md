On imbalanced data the ROC curve can look optimistic: since there are so many
negatives, even hundreds of false positives raise the FPR only a little. The
**precision-recall curve** plots precision and recall at every threshold; a
summary of the area under it is **average precision (AP)**: the weighted sum of
the precision at each point where recall increases.

```python
import numpy as np
from sklearn.metrics import average_precision_score

rng = np.random.default_rng(6)
n = 1000
y = (rng.random(n) < 0.05).astype(int)
score = rng.normal(0, 1, n) + 1.8 * y


def average_precision(y, score):
    ys = y[np.argsort(-score)]
    tp = np.cumsum(ys)
    precision = tp / np.arange(1, len(ys) + 1)
    recall = tp / ys.sum()
    gains = np.diff(np.concatenate([[0], recall]))
    return float((gains * precision).sum())


ours = average_precision(y, score)
print(round(ours, 4), round(average_precision_score(y, score), 4))
print(round(y.mean(), 3))
```

```text
0.3727 0.3727
0.04
```

AP is around 0.37; the same as scikit-learn's. A random model's AP equals the
positive rate (0.04); so the model is about nine times the baseline. The same
model scored 0.878 on ROC: on imbalanced data ROC AUC can look good while AP
looks modest. If finding the positives is the real job, AP is the more honest
summary.
