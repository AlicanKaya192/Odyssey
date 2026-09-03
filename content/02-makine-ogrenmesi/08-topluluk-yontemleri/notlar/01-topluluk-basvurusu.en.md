## Random forest

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

model = RandomForestClassifier(n_estimators=200, random_state=42)
```

| Parameter | What it does | Default |
|---|---|---|
| `n_estimators` | How many trees | 100 |
| `max_depth` | Each tree's depth | `None` |
| `min_samples_leaf` | The fewest records a leaf may hold | 1 |
| `max_features` | How many features to try per split | `sqrt` |
| `bootstrap` | Draw samples with replacement | `True` |
| `oob_score` | Compute the out-of-bag score | `False` |
| `n_jobs` | How many cores to use (`-1` for all) | `None` |
| `class_weight` | Class weights on imbalanced data | `None` |

**`max_features` is the heart of a forest.** At each split only a subset of
the features is tried; this makes the trees differ from one another. Trying
all of them turns the forest into plain bagging and the trees start to look
alike.

**`n_estimators` is not an overfitting parameter.** Raising it does not
worsen the result, only slow it down. Measured: 0.90 with 25 trees and 0.90
with 300.

## Gradient boosting

```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(
    n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
```

| Parameter | What it does |
|---|---|
| `n_estimators` | How many rounds of correction |
| `learning_rate` | Each round's contribution; small = safe but slow |
| `max_depth` | The trees are kept **shallow** (2-5 typically) |
| `subsample` | A fraction of the data per round (< 1 makes it stochastic) |

**`n_estimators` and `learning_rate` are tuned together.** Lower one and the
other has to rise. A rough starting point: `learning_rate=0.1` and
`n_estimators=100`.

**Boosting can overfit** — unlike a forest. Past a point, adding trees
lowers the test score.

The faster version:

```python
from sklearn.ensemble import HistGradientBoostingClassifier

model = HistGradientBoostingClassifier(random_state=42)
```

Far faster on large data and **it can work with missing values** — one of
the few models in sklearn that can.

## The difference between the two

| | Forest | Boosting |
|---|---|---|
| Trees | Parallel, independent | Sequential, correcting each other |
| Tree depth | Deep | Shallow |
| What it reduces | Variance | Bias |
| Overfitting | Does not grow with tree count | Can |
| Tuning | Little; the defaults work | A lot; tuned jointly |
| Speed | Parallelisable (`n_jobs`) | Sequential, not parallelisable |

## Out-of-bag score (OOB)

```python
model = RandomForestClassifier(n_estimators=200, oob_score=True,
                               random_state=42)
model.fit(X_train, y_train)
print(round(float(model.oob_score_), 3))
```

Each tree does not see roughly **a third** of the training data; the score
is computed on those rows. It gives an estimate without setting aside a
separate validation set.

Its limits: it only works with `bootstrap=True`, it is unreliable with few
trees, and **it does not replace the test set**.

## Feature importance

```python
for name, value in zip(X.columns, model.feature_importances_):
    print(name, round(float(value), 3))
```

A forest's importance is **steadier** than a single tree's: hundreds of
trees are averaged and every feature gets tried many times. Measured: a
single tree gives `age` 0.0 while the forest gives it 0.232.

The same three traps still apply: not causation, correlated columns share
importance, high-cardinality columns inflate. The more reliable route is
again `permutation_importance`.

## Speed

```python
RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
```

`n_jobs=-1` uses every core. Because the trees are independent a forest
parallelises well; **boosting does not**, since each tree waits for the
previous one.

## Common mistakes

- **Taking `n_estimators` for an overfitting knob.** Raising it is harmless
  in a forest.
- **Raising the tree count without limit in boosting.** There the
  overfitting is real.
- **Reading one test score and calling ensembles pointless.** Measured: on a
  single split the tree wins with 0.96 and loses on cross validation with
  0.827.
- **Scaling a forest.** Everything inside is a tree; unnecessary.
- **Not passing `random_state`.** A forest is built on randomness
  throughout; without it the result cannot be reproduced.
- **Expecting interpretability.** 200 trees' rules do not turn into a
  sentence.
- **Using `oob_score` in place of the test score.** OOB comes from the
  training data.
