# Resampling

We measure how good a model is on data it has **not seen**. But we have a
single data set: splitting it into training and test, splitting it again and
again, and shuffling the labels are all ways of making "another data set" out
of the same data. In this section we write these from scratch and measure how
misleading a single split can be.

## The data and a simple model

120 samples with two classes and two features. As the model we use one of the
simplest: **nearest centroid**. It learns each class's mean point (centre) and
puts a new sample into the class of the nearest centre.

```python
import numpy as np

rng = np.random.default_rng(2)
n = 120
y = (rng.random(n) < 0.3).astype(int)              # about 30% class 1
X = rng.normal(0, 1, size=(n, 2)) + y[:, None] * 1.2


def centroid_fit(X, y):
    return {c: X[y == c].mean(axis=0) for c in np.unique(y)}


def centroid_predict(centers, X):
    labels = list(centers)
    dists = np.stack([((X - centers[c]) ** 2).sum(axis=1) for c in labels])
    return np.array(labels)[dists.argmin(axis=0)]


def accuracy(y_true, y_pred):
    return (y_true == y_pred).mean()


print(np.bincount(y))
```

```text
[82 38]
```

## How reliable is a single split?

A train/test split: shuffle the indices, set a part aside for testing. Let us
split the same data with ten different seeds and train the model each time:

```python
def split(n, test_size, seed):
    order = np.random.default_rng(seed).permutation(n)
    cut = int(n * test_size)
    return order[cut:], order[:cut]                # train, test


scores = []
for seed in range(10):
    train, test = split(n, 0.25, seed)
    model = centroid_fit(X[train], y[train])
    scores.append(accuracy(y[test], centroid_predict(model, X[test])))
print(np.round(scores, 2).tolist())
print(round(min(scores), 2), round(max(scores), 2))
```

```text
[0.8, 0.73, 0.8, 0.77, 0.83, 0.8, 0.77, 0.83, 0.73, 0.77]
0.73 0.83
```

The same model, the same data: accuracy between 0.73 and 0.83. In a test set
of 30 samples, three samples changing makes a ten-point difference. Deciding
"our model is 83%, the other 78%" stays inside this unsteadiness.

## k-fold cross-validation

**k-fold cross-validation** splits the data into `k` parts; each part is the
test set once while the rest is for training, and the mean of the `k` results
is taken. Every sample is tested exactly once.

<figure class="fig">
<svg viewBox="0 0 440 175" width="440" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="60" y="28" font-size="12" text-anchor="end">fold 1</text><rect class="dot" x="70" y="10" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="103.0" y="27" font-size="11" text-anchor="middle">test</text><rect class="box" x="140" y="10" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="27" font-size="11" text-anchor="middle">train</text><rect class="box" x="210" y="10" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="27" font-size="11" text-anchor="middle">train</text><rect class="box" x="280" y="10" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="27" font-size="11" text-anchor="middle">train</text><rect class="box" x="350" y="10" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="27" font-size="11" text-anchor="middle">train</text><text class="dim" x="60" y="60" font-size="12" text-anchor="end">fold 2</text><rect class="box" x="70" y="42" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="59" font-size="11" text-anchor="middle">train</text><rect class="dot" x="140" y="42" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="173.0" y="59" font-size="11" text-anchor="middle">test</text><rect class="box" x="210" y="42" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="59" font-size="11" text-anchor="middle">train</text><rect class="box" x="280" y="42" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="59" font-size="11" text-anchor="middle">train</text><rect class="box" x="350" y="42" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="59" font-size="11" text-anchor="middle">train</text><text class="dim" x="60" y="92" font-size="12" text-anchor="end">fold 3</text><rect class="box" x="70" y="74" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="91" font-size="11" text-anchor="middle">train</text><rect class="box" x="140" y="74" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="91" font-size="11" text-anchor="middle">train</text><rect class="dot" x="210" y="74" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="243.0" y="91" font-size="11" text-anchor="middle">test</text><rect class="box" x="280" y="74" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="91" font-size="11" text-anchor="middle">train</text><rect class="box" x="350" y="74" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="91" font-size="11" text-anchor="middle">train</text><text class="dim" x="60" y="124" font-size="12" text-anchor="end">fold 4</text><rect class="box" x="70" y="106" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="123" font-size="11" text-anchor="middle">train</text><rect class="box" x="140" y="106" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="123" font-size="11" text-anchor="middle">train</text><rect class="box" x="210" y="106" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="123" font-size="11" text-anchor="middle">train</text><rect class="dot" x="280" y="106" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="313.0" y="123" font-size="11" text-anchor="middle">test</text><rect class="box" x="350" y="106" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="123" font-size="11" text-anchor="middle">train</text><text class="dim" x="60" y="156" font-size="12" text-anchor="end">fold 5</text><rect class="box" x="70" y="138" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="155" font-size="11" text-anchor="middle">train</text><rect class="box" x="140" y="138" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="155" font-size="11" text-anchor="middle">train</text><rect class="box" x="210" y="138" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="155" font-size="11" text-anchor="middle">train</text><rect class="box" x="280" y="138" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="155" font-size="11" text-anchor="middle">train</text><rect class="dot" x="350" y="138" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="383.0" y="155" font-size="11" text-anchor="middle">test</text></svg>
<figcaption>5-fold cross-validation: each row is one training; the coloured part is that round's test. Every sample is tested exactly once.</figcaption>
</figure>

```python
def kfold(n, k):
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    start = 0
    for size in sizes:
        test = np.arange(start, start + size)
        train = np.concatenate([np.arange(0, start), np.arange(start + size, n)])
        yield train, test
        start += size


from sklearn.model_selection import KFold

ours = [t.tolist() for _, t in kfold(n, 5)]
theirs = [t.tolist() for _, t in KFold(n_splits=5).split(X)]
print(ours == theirs, [len(t) for t in ours])


def cv_score(X, y, k, seed):
    order = np.random.default_rng(seed).permutation(len(y))
    Xs, ys = X[order], y[order]
    accs = []
    for train, test in kfold(len(ys), k):
        model = centroid_fit(Xs[train], ys[train])
        accs.append(accuracy(ys[test], centroid_predict(model, Xs[test])))
    return np.mean(accs)


cv = [cv_score(X, y, 5, seed) for seed in range(10)]
print(round(min(cv), 3), round(max(cv), 3))
print(round(np.std(scores), 3), round(np.std(cv), 3))
```

```text
True [24, 24, 24, 24, 24]
0.767 0.783
0.034 0.006
```

Our folds are exactly the same as scikit-learn's `KFold`. Over ten different
shuffles the 5-fold result stayed between 0.767 and 0.783; its standard
deviation (0.006) is about a fifth of the single split's (0.034). The price:
the model is trained five times instead of once.

## Stratified splitting

If the classes are imbalanced (82 to 38 here), the minority class sometimes
falls into a random test set rarely, sometimes often. **Stratified** splitting
splits each class within itself; the proportions in the test set stay as in
the whole data.

```python
def stratified_split(y, test_size, seed):
    rng = np.random.default_rng(seed)
    train, test = [], []
    for c in np.unique(y):
        idx = rng.permutation(np.flatnonzero(y == c))
        cut = round(len(idx) * test_size)
        test.extend(idx[:cut])
        train.extend(idx[cut:])
    return np.array(train), np.array(test)


plain = [int(y[split(n, 0.25, s)[1]].sum()) for s in range(10)]   # class 1 count
strat = [int(y[stratified_split(y, 0.25, s)[1]].sum()) for s in range(10)]
print(plain)
print(strat)
```

```text
[10, 14, 7, 9, 12, 5, 13, 10, 13, 10]
[10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
```

With a random split, a test set of 30 has between 5 and 14 samples of class 1;
with a stratified split, 10 every time. The smaller the minority class, the
more this matters: for classification scikit-learn uses `StratifiedKFold`.

## Permutation test: did the model learn anything?

The accuracy is 0.775. Could it be by chance? A **permutation test** shuffles
the labels (breaking their link to the features) and repeats the same
measurement hundreds of times. If the real result beats most of these
"meaningless" results, the model really learned something.

```python
real = cv_score(X, y, 5, 0)
fake = []
perm_rng = np.random.default_rng(9)
for _ in range(200):
    fake.append(cv_score(X, perm_rng.permutation(y), 5, 0))
p_value = (np.sum(np.array(fake) >= real) + 1) / (len(fake) + 1)
print(round(real, 3), round(np.mean(fake), 3), round(max(fake), 3))
print(round(p_value, 4))
```

```text
0.775 0.506 0.617
0.005
```

With shuffled labels the accuracy is 0.506 on average and 0.617 at best; the
real result (0.775) is nowhere near any of them. The p-value is `1/201` ≈
0.005: this result is very unlikely to be a coincidence.

## Summary

- A single train/test split is unsteady: 0.73 to 0.83 for the same model.
- k-fold cross-validation tests every sample once; its result is much steadier,
  the price is `k` times the training.
- With imbalanced classes, stratified splitting keeps the proportions.
- A permutation test measures whether the result beats chance.
- The scaler and the model are `fit` in each fold **only on that fold's
  training part**; otherwise data leaks.
