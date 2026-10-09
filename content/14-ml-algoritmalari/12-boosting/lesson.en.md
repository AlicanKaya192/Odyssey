# Boosting

Bagging built independent trees side by side and let them vote. **Boosting**
builds trees **in sequence**: each new model focuses on the error the previous
ones still make. Models that are weak (shallow) on their own turn into a strong
one. Many of the most successful methods on tabular data (XGBoost, LightGBM,
CatBoost) are accelerated versions of this idea.

## Gradient boosting: trees on residuals

In regression the idea is very plain: first predict the mean for everyone.
Then fit a small tree to the **residuals** (true − predicted) and add a small
part (`lr`, the learning rate) of the tree's output to the prediction. Repeat.
With the squared error, the residual is the negative of the loss's gradient;
that is where the name comes from.

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(12)
X = rng.uniform(0, 10, (200, 1))
y = np.sin(X[:, 0]) * 3 + 0.3 * X[:, 0] + rng.normal(0, 0.5, 200)
Xt = rng.uniform(0, 10, (1000, 1))
yt = np.sin(Xt[:, 0]) * 3 + 0.3 * Xt[:, 0] + rng.normal(0, 0.5, 1000)


def boost(X, y, n_trees, lr, depth=2):
    start = y.mean()
    pred = np.full(len(y), start)
    trees = []
    for _ in range(n_trees):
        resid = y - pred                                # the error so far
        tree = DecisionTreeRegressor(max_depth=depth).fit(X, resid)
        # fix part of the error
        pred += lr * tree.predict(X)
        trees.append(tree)
    return start, trees


def boost_predict(model, X, lr):
    start, trees = model
    return start + lr * sum(t.predict(X) for t in trees)


def mse(a, b):
    return ((a - b) ** 2).mean()


for n in (1, 10, 50, 200):
    m = boost(X, y, n, 0.1)
    train = mse(y, boost_predict(m, X, 0.1))
    test = mse(yt, boost_predict(m, Xt, 0.1))
    print(n, round(train, 3), round(test, 3))
from sklearn.ensemble import GradientBoostingRegressor

m = boost(X, y, 100, 0.1)
ref = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=2,
                                random_state=0).fit(X, y)
print(np.allclose(boost_predict(m, Xt, 0.1), ref.predict(Xt)))
```

```text
1 3.985 3.914
10 1.379 1.252
50 0.217 0.321
200 0.095 0.342
True
```

With one tree the test error is 3.9; with 50 trees 0.32. Our predictions are
exactly the same as scikit-learn's `GradientBoostingRegressor`. But note: at 200
trees, while the training error keeps falling (0.095), the test error rises
again (0.342). Unlike bagging, in boosting **adding trees can overfit**; the
number of trees is chosen with cross-validation or early stopping.

## Learning rate: small steps

```python
for lr in (1.0, 0.1):
    m = boost(X, y, 300, lr, depth=3)
    train = mse(y, boost_predict(m, X, lr))
    test = mse(yt, boost_predict(m, Xt, lr))
    print(lr, round(train, 3), round(test, 3))
```

```text
1.0 0.0 0.534
0.1 0.021 0.425
```

`lr = 1` adds each tree's prediction in full: training error 0, test 0.534
(memorisation). `lr = 0.1` adds only a tenth each time: test 0.425. A small rate
and more trees is usually the model that generalises better (**shrinkage**).

## AdaBoost: weigh the mistakes up

The first famous form of boosting in classification is **AdaBoost**. In each
round a one-question tree (a decision stump) is trained with sample weights;
the weight of misclassified samples is raised, so the next stump looks at them.
Each stump's vote is weighted by a coefficient (`α`) based on its error.

```python
from sklearn.tree import DecisionTreeClassifier

Xc = rng.uniform(-3, 3, (300, 2))
yc = (Xc[:, 0] ** 2 + Xc[:, 1] ** 2 < 4).astype(int)   # inside a circle: 1
Xct = rng.uniform(-3, 3, (1000, 2))
yct = (Xct[:, 0] ** 2 + Xct[:, 1] ** 2 < 4).astype(int)


def adaboost(X, y, rounds):
    s = np.where(y == 1, 1, -1)
    w = np.full(len(y), 1 / len(y))
    stumps, alphas = [], []
    for _ in range(rounds):
        stump = DecisionTreeClassifier(max_depth=1).fit(X, y, sample_weight=w)
        h = np.where(stump.predict(X) == 1, 1, -1)
        err = w[h != s].sum() / w.sum()
        # little error, a big vote
        alpha = np.log((1 - err) / err)
        # weigh the mistakes up
        w = w * np.exp(alpha * (h != s))
        w /= w.sum()
        stumps.append(stump)
        alphas.append(alpha)
    return stumps, alphas


def ada_predict(model, X):
    stumps, alphas = model
    score = 0
    for stump, alpha in zip(stumps, alphas):
        score = score + alpha * np.where(stump.predict(X) == 1, 1, -1)
    return (score > 0).astype(int)


from sklearn.ensemble import AdaBoostClassifier

model = adaboost(Xc, yc, 50)
ref = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=50)
ref.fit(Xc, yc)
ours = ada_predict(model, Xct)
print((ours == ref.predict(Xct)).mean())
one = DecisionTreeClassifier(max_depth=1).fit(Xc, yc)
print(round((one.predict(Xct) == yct).mean(), 3), round((ours == yct).mean(), 3))
```

```text
1.0
0.644 0.948
```

The class is the inside of a circle; a single stump can draw only one line
perpendicular to an axis and stays at 64.4%. The weighted vote of fifty stumps
wraps the circle with many lines: 94.8%. Our predictions match scikit-learn's
`AdaBoostClassifier`.

## Summary

- Boosting builds models in sequence; each new model focuses on the previous
  ones' error.
- Gradient boosting: start from the mean, each round a shallow tree on the
  residuals, add `lr` of it.
- In boosting, the number of trees can overfit; it is chosen with early
  stopping or cross-validation.
- A small learning rate + more trees usually generalises better.
- AdaBoost: weigh misclassified samples up and let stumps vote by their errors.
