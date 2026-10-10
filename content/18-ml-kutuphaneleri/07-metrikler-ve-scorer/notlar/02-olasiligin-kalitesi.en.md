AUC looks at the **order** of the probabilities, not their values. Whether a
model that says "30% risk" is really right in 30 cases out of 100 is measured
by the **Brier score**: the mean of the squared difference between the
probability and the real outcome (0 or 1). Smaller is better.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.95], flip_y=0.02, random_state=7)
print(round(y.mean() * (1 - y.mean()), 4))
for model in [LogisticRegression(), DecisionTreeClassifier(random_state=0)]:
    auc = cross_val_score(model, X, y, cv=5, scoring="roc_auc").mean()
    brier = -cross_val_score(model, X, y, cv=5, scoring="neg_brier_score").mean()
    print(type(model).__name__, round(auc, 3), round(brier, 4))
brier_scorer = make_scorer(brier_score_loss, greater_is_better=False,
                           response_method="predict_proba")
scores = cross_val_score(LogisticRegression(), X, y, cv=5, scoring=brier_scorer)
print(round(-scores.mean(), 4))
```

```text
0.0564
LogisticRegression 0.849 0.0376
DecisionTreeClassifier 0.747 0.0585
0.0376
```

## What we see

- The first line is the baseline: a model that gives everyone the same
  probability (the positive rate) gets 0.0564.
- Logistic regression 0.0376: its probabilities mean something.
- The unlimited-depth tree gives a probability of 0 or 1 in every leaf; Brier
  0.0585, that is **worse than the baseline**. When it is wrong, it is wrong
  with full confidence. Its AUC is also lower (0.747).
- If your own scorer needs probabilities, `response_method="predict_proba"`:
  `brier_scorer` gave the same number as the built-in `"neg_brier_score"`.

## When it matters

- When the probability enters a decision directly (risk, price, expected
  cost).
- When a threshold is to be chosen: the threshold sits on top of the
  probability; if the probability is bad, so is the threshold.
