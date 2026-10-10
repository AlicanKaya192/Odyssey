Boosting's two main settings are tied together: the **learning rate** is how
much of each tree's correction is taken, the **number of trees** is how many
corrections are made. Small steps need more steps.

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=20000, n_features=20, n_informative=8,
                           flip_y=0.05, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
for rate, trees in [(0.3, 100), (0.1, 100), (0.03, 100), (0.03, 600)]:
    model = HistGradientBoostingClassifier(learning_rate=rate, max_iter=trees,
                                           early_stopping=False, random_state=0)
    print(rate, trees, round(model.fit(X_train, y_train).score(X_test, y_test), 3))
```

```text
0.3 100 0.954
0.1 100 0.955
0.03 100 0.948
0.03 600 0.957
```

## What we see

- With 100 trees, 0.3 and 0.1 are about the same (0.954, 0.955). 0.03 cannot
  catch up in 100 trees: 0.948; the model is still near the start.
- The same small rate with 600 trees gave the best result: 0.957. Small
  steps, if enough of them are taken, usually arrive somewhere a little
  better.
- The price is time: 600 trees are 6 times the work of 100.

## The rule

- When you lower the rate, raise the number of trees; rather than searching
  both separately, fix the rate (0.05–0.1) and leave the number of trees to
  early stopping.
- The difference is small (0.955 vs 0.957); working on the data and features
  first often gains more.
