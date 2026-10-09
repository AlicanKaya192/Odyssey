# Bagging and Random Forests

At the end of section 10 we saw that a deep tree is unstable and overfits. The
cure is surprisingly simple: **build many trees and let them vote**. If each
tree sees a slightly different version of the data, their errors differ too;
on average they cancel out. In this section we build the ensemble from
scratch; for the individual trees we use scikit-learn's
`DecisionTreeClassifier`, the fast counterpart of what we wrote in section 10,
as the building block.

## Bagging: bootstrap + voting

**Bagging** (bootstrap aggregating): each tree is trained on a sample of the
same size drawn **with replacement** from the training data (the bootstrap of
ALG 2); the prediction is the trees' majority vote.

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(11)


def make(n):
    # the last three are noise
    X = rng.uniform(0, 10, (n, 6))
    score = np.sin(X[:, 0]) * 2 + (X[:, 1] - 5) * 0.6 + (X[:, 2] > 5)
    y = (score + rng.normal(0, 1.0, n) > 0.5).astype(int)
    return X, y


X, y = make(400)
Xt, yt = make(2000)

single = DecisionTreeClassifier(random_state=0).fit(X, y)
print(round((single.predict(Xt) == yt).mean(), 3))


def bagging(X, y, n_trees, seed, max_features=None):
    boot_rng = np.random.default_rng(seed)
    trees, bags = [], []
    for i in range(n_trees):
        idx = boot_rng.integers(0, len(y), len(y))     # with replacement
        tree = DecisionTreeClassifier(max_features=max_features, random_state=i)
        trees.append(tree.fit(X[idx], y[idx]))
        bags.append(idx)
    return trees, bags


def vote(trees, X):
    votes = np.array([t.predict(X) for t in trees])
    return (votes.mean(axis=0) > 0.5).astype(int)


for n in (1, 5, 25, 100):
    trees, _ = bagging(X, y, n, 0)
    print(n, round((vote(trees, Xt) == yt).mean(), 3))
```

```text
0.738
1 0.732
5 0.764
25 0.782
100 0.8
```

A single deep tree scores 0.738. As the number of trees grows the vote gets
stronger: 0.80 with 100 trees. No single tree is better on its own; the gain
comes from the errors being different. Adding trees does not cause
overfitting, it only adds computing time.

## Random forest: shuffle the features too

If there is one strong feature, every tree asks about it first and the trees
look alike; the vote of similar trees gains little. A **random forest** looks
at only a random subset of the features at each split (usually `√d` of them in
classification). The trees become more different from each other.

```python
bag_trees, bags = bagging(X, y, 100, 0)
rf_trees, rf_bags = bagging(X, y, 100, 0, max_features="sqrt")
print(round((vote(rf_trees, Xt) == yt).mean(), 3))


def mean_agreement(trees, X):
    P = np.array([t.predict(X) for t in trees[:30]])
    pairs = [(P[i] == P[j]).mean() for i in range(30) for j in range(i + 1, 30)]
    return round(float(np.mean(pairs)), 3)


print(mean_agreement(bag_trees, Xt), mean_agreement(rf_trees, Xt))
from sklearn.ensemble import RandomForestClassifier

ref = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)
print(round((ref.predict(Xt) == yt).mean(), 3))
```

```text
0.814
0.751 0.704
0.809
```

The random forest scores 0.814; scikit-learn's `RandomForestClassifier` 0.809
(not exactly the same since its random choices differ, but in the same place).
The second line shows why: two bagging trees give the same prediction on
75.1% of the test on average, two random forest trees on 70.4%. More
independent trees, a stronger vote.

## Out-of-bag (OOB) validation

With the bootstrap, each tree never sees about a third of the samples. If we
predict each sample only with the vote of the trees that **did not see** it, we
get a validation measure without a separate test set: **out-of-bag (OOB)**.

```python
def oob_score(trees, bags, X, y):
    votes, counts = np.zeros(len(y)), np.zeros(len(y))
    for tree, idx in zip(trees, bags):
        # what this tree did not see
        out = np.setdiff1d(np.arange(len(y)), idx)
        votes[out] += tree.predict(X[out])
        counts[out] += 1
    seen = counts > 0
    pred = (votes[seen] / counts[seen] > 0.5).astype(int)
    return round(float((pred == y[seen]).mean()), 3)


n = len(y)
unseen = np.mean([n - len(np.unique(b)) for b in rf_bags]) / n
print(oob_score(rf_trees, rf_bags, X, y), round(float(unseen), 3))
```

```text
0.828 0.364
```

The OOB accuracy is 0.828; on the separate 2000-sample test 0.814. Close: OOB is
a free estimate without splitting the data. The share each tree did not see is
0.364, that is about `1/e`.

## Which feature matters? Permutation importance

Shuffle one feature's values in the test data; a model relying on that feature
breaks, while nothing changes for an unimportant feature.

```python
base = (vote(rf_trees, Xt) == yt).mean()
perm_rng = np.random.default_rng(1)
for j in range(6):
    Xp = Xt.copy()
    Xp[:, j] = perm_rng.permutation(Xp[:, j])
    print(j, round(base - (vote(rf_trees, Xp) == yt).mean(), 3))
```

```text
0 0.049
1 0.27
2 0.012
3 0.001
4 -0.002
5 0.005
```

When `x₁` is shuffled, accuracy drops by 0.27: the most important feature.
`x₀` 0.049, `x₂` 0.012; the last three (noise) around zero. Consistent with the
formula that generated the data. Permutation importance works with any model
and directly answers "what do I lose without this feature?".

## Summary

- Bagging: trees on bootstrap samples, a majority vote; errors cancel out.
- Random forest: a random feature subset at each split; trees more
  independent, the vote stronger.
- Adding trees does not overfit; it only slows things down.
- OOB: predict each sample with the trees that did not see it; validation
  without a separate test set.
- Permutation importance: how much is lost when a feature is shuffled?
