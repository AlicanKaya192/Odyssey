# Writing It from Scratch

In ALG 3 we will write machine learning algorithms **from scratch with NumPy**
and compare each with scikit-learn's result. The aim is not to replace
scikit-learn: someone who knows what is inside a model tunes it correctly,
diagnoses its errors and knows its limits. The answer to "why did this model
predict that?" is often in twenty lines of code.

This section builds three habits: thinking of data as an **array**, writing
**vector operations** instead of loops, and building every model with the same
**`fit` / `predict`** pattern.

## Data is a matrix

In machine learning, data is almost always a **matrix**: each row is a sample
(an observation), each column a feature. In NumPy it is called `X`, with shape
`(number of samples, number of features)`.

```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(loc=[50, 3], scale=[10, 0.5], size=(200, 2))
print(X.shape)
print(X[:2].round(2))
print(X.mean(axis=0).round(2), X.std(axis=0).round(2))
```

```text
(200, 2)
[[51.26  2.93]
 [56.4   3.05]]
[49.02  3.01] [9.79 0.5 ]
```

`default_rng(0)` is a seeded generator: anyone running the same code sees the
same numbers. `axis=0` means "along the rows", that is, **per column**: the
mean and standard deviation of the two features.

<figure class="fig">
<svg viewBox="0 0 430 270" width="430" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="70" y="40" width="46" height="46"/><rect class="box" x="116" y="40" width="46" height="46"/><rect class="box" x="162" y="40" width="46" height="46"/><rect class="box" x="70" y="86" width="46" height="46"/><rect class="box" x="116" y="86" width="46" height="46"/><rect class="box" x="162" y="86" width="46" height="46"/><rect class="box" x="70" y="132" width="46" height="46"/><rect class="box" x="116" y="132" width="46" height="46"/><rect class="box" x="162" y="132" width="46" height="46"/><rect class="box" x="70" y="178" width="46" height="46"/><rect class="box" x="116" y="178" width="46" height="46"/><rect class="box" x="162" y="178" width="46" height="46"/><text class="dim" x="93.0" y="30" font-size="12" text-anchor="middle">feat. 1</text><text class="dim" x="139.0" y="30" font-size="12" text-anchor="middle">feat. 2</text><text class="dim" x="185.0" y="30" font-size="12" text-anchor="middle">feat. 3</text><text class="dim" x="62" y="67.0" font-size="12" text-anchor="end">sample 1</text><text class="dim" x="62" y="113.0" font-size="12" text-anchor="end">sample 2</text><text class="dim" x="62" y="159.0" font-size="12" text-anchor="end">sample 3</text><text class="dim" x="62" y="205.0" font-size="12" text-anchor="end">sample 4</text><line class="curve" x1="93.0" y1="46" x2="93.0" y2="238"/><polygon class="dot" points="87.0,238 99.0,238 93.0,248"/><text class="ink" x="70" y="266" font-size="13">axis=0: per column</text><line class="curve2" x1="76" y1="63.0" x2="224" y2="63.0"/><polygon class="dot2" points="224,57.0 224,69.0 234,63.0"/><text class="ink" x="240" y="68.0" font-size="13">axis=1: per row</text></svg>
<figcaption><code>X.mean(axis=0)</code> moves along the rows and gives one number per column; <code>axis=1</code> one number per row.</figcaption>
</figure>

## Vector operations, not loops

A linear model's prediction for each row is `w₁x₁ + w₂x₂ + w₃x₃`. You can
write it with a Python loop or with a single matrix product (`X @ w`):

```python
import time

big = rng.normal(size=(1_000_000, 3))
w = np.array([0.5, -2.0, 1.0])
t = time.perf_counter()
loop = [row[0] * w[0] + row[1] * w[1] + row[2] * w[2] for row in big]
t_loop = time.perf_counter() - t
t = time.perf_counter()
vec = big @ w
t_vec = time.perf_counter() - t
print(np.allclose(loop, vec), round(t_loop / t_vec))
```

```text
True 195
```

The results are the same (`np.allclose` compares while tolerating small
rounding differences); but on this computer the loop is more than a hundred
times slower. NumPy's operations are written in C and process the whole array
at once. The rule in this module: **array operations instead of row-by-row
loops**. Loops remain only for the algorithm's own steps (gradient descent's
rounds, a tree's nodes).

## The `fit` / `predict` pattern

Every model in scikit-learn follows the same contract: `fit(X, y)` learns from
the data and stores what it learned in attributes ending with `_` (`mean_`,
`coef_`); `transform` or `predict` applies what it learned to new data. We will
do the same. The first example is a **standardiser** that scales the features
to mean 0 and standard deviation 1:

```python
class Standardizer:
    def fit(self, X):
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        return self                    # chaining: .fit(X).transform(X)

    def transform(self, X):
        return (X - self.mean_) / self.scale_


from sklearn.preprocessing import StandardScaler

mine = Standardizer().fit(X).transform(X)
theirs = StandardScaler().fit(X).transform(X)
print(np.allclose(mine, theirs))
print(mine.mean(axis=0).round(6) + 0, mine.std(axis=0).round(6))
sample_std = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
print(np.allclose(sample_std, theirs), np.abs(sample_std - theirs).max().round(4))
```

```text
True
[0. 0.] [1. 1.]
False 0.0094
```

Ours matches scikit-learn's. In the line `X - self.mean_`, **broadcasting**
is at work: when a `(2,)` vector is subtracted from a `(200, 2)` matrix, NumPy
applies the vector to every row.

The last line is a small trap: in statistics the sample standard deviation is
divided by `n − 1` (`ddof=1`), while scikit-learn divides by `n` (`ddof=0`).
The difference is small, but the result is no longer the same. Writing from
scratch, details like this are caught by comparing.

## The simplest model: the majority class

The first question before evaluating a classifier: "how successful is a model
that always says the most frequent class?" This is a **baseline**; the model
has to beat it.

```python
from collections import Counter


class MajorityClassifier:
    def fit(self, X, y):
        self.label_ = Counter(y).most_common(1)[0][0]
        return self

    def predict(self, X):
        return np.full(len(X), self.label_)


from sklearn.dummy import DummyClassifier

y = (X[:, 0] > 55).astype(int)
ours = MajorityClassifier().fit(X, y).predict(X)
ref = DummyClassifier(strategy="most_frequent").fit(X, y).predict(X)
print(np.bincount(y), (ours == ref).all(), (ours == y).mean())
```

```text
[145  55] True 0.725
```

145 of the 200 samples are in class 0; a model always saying "0" is 72.5%
right. A model with 75% accuracy looks good at first sight, but it only just
beats the baseline. In section 6 we will see why accuracy alone is misleading.

## Summary

- Data is a matrix: rows are samples, columns are features; `axis=0` is per
  column.
- Array operations instead of loops (`X @ w`, `X.mean(axis=0)`); on this
  computer more than a hundred times faster.
- `fit` learns and writes to attributes ending with `_`; `transform` /
  `predict` apply it; `fit` returns `self`.
- Every model written from scratch is compared with scikit-learn using
  `np.allclose` or `==`; if there is a difference, the reason is a detail
  (like `ddof`).
- Baseline: the model that always says the most frequent class.
