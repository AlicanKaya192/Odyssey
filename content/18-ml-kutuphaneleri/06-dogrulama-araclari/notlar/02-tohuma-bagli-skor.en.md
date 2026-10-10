When splitting with shuffling, the score depends on `random_state`. Same
model, same data, only the seed changes:

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (RepeatedStratifiedKFold, StratifiedKFold,
                                     cross_val_score)

X, y = make_classification(n_samples=400, n_features=10, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
model = LogisticRegression()
for seed in range(3):
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    print(seed, round(cross_val_score(model, X, y, cv=cv).mean(), 3))
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=0)
scores = cross_val_score(model, X, y, cv=cv)
print(len(scores), round(scores.mean(), 3), round(scores.std(), 3))
```

```text
0 0.825
1 0.817
2 0.827
50 0.825 0.027
```

## What we see

- Over three seeds the mean moves between 0.817 and 0.827. If you see a 0.01
  difference between two models, check whether it is bigger than this
  movement.
- `RepeatedStratifiedKFold` does the 5-fold split 10 times, each with a
  different shuffle: 50 scores. Mean 0.825, spread across folds 0.027.
- Repeating does not improve the model; it only frees the mean from one lucky
  or unlucky split. The price is 10 times the training.

## When

- When the data is small (a few hundred rows) and the models are close.
- When a report should say "mean ± spread" instead of one number.
- With large data a single 5-fold split is usually enough.
