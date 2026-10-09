# Decision Trees

A **decision tree** splits the data with yes/no questions: "is x₀ ≤ 5.97?" Each
question divides the data in two, and a prediction sits in each leaf. Prediction
is a walk from the root to a leaf (the trees of ALG 1). The model is readable,
needs no scaling, and handles numbers and categories together. In this section
we write the **CART** algorithm that scikit-learn uses, from scratch.

## The purity measure: Gini

A good question leaves both sides as "pure" (single-class) as possible. The
**Gini impurity** is `1 − Σ pₖ²`: 0 for a single-class group, 0.5 if two classes
are half and half. The value of a split is the average of the two sides' Gini,
weighted by the number of samples; the smallest is chosen. The candidate
thresholds are the midpoints of a feature's sorted distinct values.

```python
import numpy as np

rng = np.random.default_rng(10)


def make(n):
    X = rng.uniform(0, 10, (n, 3))
    y = ((X[:, 0] > 6) | ((X[:, 1] > 7) & (X[:, 0] > 3))).astype(int)
    flip = rng.random(n) < 0.1                         # 10% noise
    return X, np.where(flip, 1 - y, y)


X, y = make(300)
Xt, yt = make(1000)


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y, minlength=2) / len(y)
    return 1 - (p ** 2).sum()


def best_split(X, y):
    best = (None, None, gini(y))
    for j in range(X.shape[1]):
        values = np.unique(X[:, j])
        for t in (values[:-1] + values[1:]) / 2:       # midpoints
            left = X[:, j] <= t
            gl, gr = gini(y[left]), gini(y[~left])
            g = (left.sum() * gl + (~left).sum() * gr) / len(y)
            if g < best[2] - 1e-12:
                best = (j, t, g)
    return best


j, t, g = best_split(X, y)
print(j, round(t, 3), round(gini(y), 4), round(g, 4))
```

```text
0 5.969 0.5 0.2856
```

The data was generated with the rule `x₀ > 6` (plus a part depending on `x₁`
and noise). The best first question is `x₀ ≤ 5.969`: the Gini fell from 0.5 to
0.286.

## Growing the tree

Ask the same question again on both sides (recursion), and put a leaf when the
depth limit or a pure group is reached: a leaf is the majority class of the
group.

```python
def build(X, y, depth, max_depth):
    if depth == max_depth or gini(y) == 0:
        return {"leaf": int(np.bincount(y, minlength=2).argmax())}
    j, t, g = best_split(X, y)
    if j is None:
        return {"leaf": int(np.bincount(y, minlength=2).argmax())}
    left = X[:, j] <= t
    return {"feature": j, "threshold": t,
            "left": build(X[left], y[left], depth + 1, max_depth),
            "right": build(X[~left], y[~left], depth + 1, max_depth)}


def predict_one(node, x):
    # from the root to a leaf
    while "leaf" not in node:
        go_left = x[node["feature"]] <= node["threshold"]
        node = node["left"] if go_left else node["right"]
    return node["leaf"]


def predict(tree, X):
    return np.array([predict_one(tree, x) for x in X])


def show(node, indent=""):
    if "leaf" in node:
        print(f"{indent}return {node['leaf']}")
        return
    print(f"{indent}if x{node['feature']} <= {node['threshold']:.2f}:")
    show(node["left"], indent + "    ")
    print(f"{indent}else:")
    show(node["right"], indent + "    ")


from sklearn.tree import DecisionTreeClassifier

tree = build(X, y, 0, 2)
show(tree)
tree = build(X, y, 0, 3)
ref = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)
print(ref.tree_.feature[0], round(ref.tree_.threshold[0], 3))
pt = predict(tree, Xt)
print((pt == ref.predict(Xt)).mean(), round((pt == yt).mean(), 3))
```

```text
if x0 <= 5.97:
    if x1 <= 7.16:
        return 0
    else:
        return 0
else:
    if x0 <= 9.89:
        return 1
    else:
        return 0
0 5.969
1.0 0.895
```

The two-level tree is a readable list of rules. Our three-level tree's root is
the same as scikit-learn's (`x₀`, 5.969), and it gives the same prediction on
all thousand test samples; accuracy 0.895.

## Depth: the knob of overfitting

```python
for depth in (1, 2, 3, 5, 10, 20):
    tr = build(X, y, 0, depth)
    acc_train = (predict(tr, X) == y).mean()
    acc_test = (predict(tr, Xt) == yt).mean()
    print(depth, round(acc_train, 3), round(acc_test, 3))
```

```text
1 0.823 0.819
2 0.823 0.811
3 0.89 0.895
5 0.933 0.855
10 1.0 0.81
20 1.0 0.81
```

As the depth grows, training accuracy rises to 1: the tree opens its own leaf
for every noisy sample. The test accuracy, however, is best at depth 3 (0.895)
and falls to 0.81 at depth 10. An unlimited tree memorises the training data;
it is limited by depth, the minimum samples per leaf (`min_samples_leaf`) or
pruning. The next section brings another cure: the average of many trees.

## Summary

- A tree splits the data with "feature ≤ threshold" questions; prediction is a
  walk from root to leaf.
- At each node CART looks for the feature and threshold that lower the Gini
  most; candidate thresholds are midpoints.
- The model is greedy: it picks the best split at each node and never goes
  back.
- As depth grows, training accuracy rises to 1 and test accuracy falls:
  overfitting.
- No scaling needed; a tree gives readable rules.
