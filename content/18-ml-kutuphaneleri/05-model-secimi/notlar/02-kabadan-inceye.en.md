The right value of settings like `C` and `gamma` may be 0.001 or 1000. An
evenly spaced grid (1, 2, 3, ...) cannot cover that width. The usual way:
first a **coarse grid on a log scale**, then a **fine** grid around the best
point.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

X, y = make_classification(n_samples=400, n_features=10, n_informative=4,
                           random_state=12)
coarse = {"C": np.logspace(-3, 3, 7), "gamma": np.logspace(-4, 1, 6)}
first = GridSearchCV(SVC(), coarse, cv=5).fit(X, y)
c0, g0 = first.best_params_["C"], first.best_params_["gamma"]
print(round(float(c0), 4), round(float(g0), 4), round(first.best_score_, 3))
steps = np.logspace(-0.5, 0.5, 5)
fine = {"C": c0 * steps, "gamma": g0 * steps}
second = GridSearchCV(SVC(), fine, cv=5).fit(X, y)
best = second.best_params_
c1, g1 = float(best["C"]), float(best["gamma"])
print(round(c1, 3), round(g1, 4), round(second.best_score_, 3))
print(len(first.cv_results_["params"]) + len(second.cv_results_["params"]))
```

```text
10.0 0.1 0.952
31.623 0.0316 0.962
67
```

## The steps

1. **Coarse:** `np.logspace(-3, 3, 7)` = 0.001, 0.01, ..., 1000. Each step is
   10 times. Among 42 combinations the best is `C=10`, `gamma=0.1`.
2. **Fine:** half a decade (√10 ≈ 3.16 times) below and above that point, 5
   values each. The best is `C≈31.6`, `gamma≈0.032`; the score rose from
   0.952 to 0.962.
3. 67 combinations in total. Searching the whole range at the same fineness
   with a single grid would take hundreds.

## Careful

- If the best value falls on the **edge** of the coarse grid (like `C=1000`),
  the range was not enough; widen it in that direction.
- The gain from the fine search (0.01 here) is often smaller than the spread
  across folds and adds to the optimism. The region the coarse search finds is
  often enough.
