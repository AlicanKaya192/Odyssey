# Naive Bayes

**Naive Bayes** applies Bayes' rule to classification: a sample's class is the
one that makes `P(class) · P(features | class)` largest. The "naive" assumption
is this: once the class is known, the features are **independent** of each
other. So `P(features | class)` splits into the product of each feature's own
probability and the model learns just by counting, in one pass. The assumption
is rarely true in reality, but the model works surprisingly well; especially on
text.

## Gaussian Naive Bayes

For continuous features a normal distribution is assumed for each class and
each feature: the mean and variance within the class. The prediction is the
largest `log P(class) + Σ log N(xᵢ | meanᵢ, varᵢ)` over the classes.

```python
import numpy as np

rng = np.random.default_rng(9)
y = rng.integers(0, 2, 200)
shift = np.where(y[:, None] == 1, [2.0, 1.0], [0.0, -1.0])
X = rng.normal(0, 1, (200, 2)) * [1.0, 2.0] + shift


def gnb_fit(X, y):
    classes = np.unique(y)
    # scikit-learn's small margin
    eps = 1e-9 * X.var(axis=0).max()
    prior = np.array([(y == c).mean() for c in classes])
    mean = np.array([X[y == c].mean(axis=0) for c in classes])
    var = np.array([X[y == c].var(axis=0) for c in classes]) + eps
    return classes, prior, mean, var


def gnb_log_posterior(model, X):
    classes, prior, mean, var = model
    diff = X[:, None, :] - mean[None]
    norm = np.log(2 * np.pi * var)[None]
    ll = -0.5 * (norm + diff ** 2 / var[None]).sum(axis=2)
    return np.log(prior)[None] + ll


from sklearn.naive_bayes import GaussianNB

model = gnb_fit(X, y)
logp = gnb_log_posterior(model, X)
pred = model[0][logp.argmax(axis=1)]
ref = GaussianNB().fit(X, y)
print((pred == ref.predict(X)).mean(), round((pred == y).mean(), 3))
proba = np.exp(logp - logp.max(axis=1, keepdims=True))
proba /= proba.sum(axis=1, keepdims=True)
print(np.allclose(proba, ref.predict_proba(X)))
```

```text
1.0 0.855
True
```

The predictions and probabilities match scikit-learn's `GaussianNB`. For that
we also added the small margin it adds to the variance (`var_smoothing`, a
billionth of the largest variance). "Learning" is just computing the mean and
variance per class: `O(n · d)`.

## Why logarithms?

Probabilities are multiplied; with hundreds of features (like the words in a
text), the product falls below the smallest number the computer can show:

```python
probs = np.full(400, 0.01)
print(np.prod(probs), round(np.log(probs).sum(), 2))
```

```text
0.0 -1842.07
```

`0.01` multiplied 400 times is 10⁻⁸⁰⁰: exactly **0** for a `float`
(underflow); when all classes are zero, no decision can be made. Logarithms are
added, and −1842 is stored easily. If probabilities are needed, the largest is
subtracted at the end and the exponential taken (like `proba` above).

## Multinomial Naive Bayes: text

On text the features are word counts. For each class, "each word's share in
this class's texts" is learned. If a word never seen in a class gets a share of
0, every text containing that word is ruled out of that class; to prevent this,
1 is added to every count (**Laplace smoothing**, `alpha = 1`).

```python
docs = ["win money now", "win a free prize now", "free money offer",
        "meeting at noon", "project meeting notes", "lunch at noon today",
        "free lunch offer", "notes for the project"]
labels = np.array([1, 1, 1, 0, 0, 0, 1, 0])          # 1: spam
vocab = sorted({w for d in docs for w in d.split()})
index = {w: i for i, w in enumerate(vocab)}


def counts(texts):
    M = np.zeros((len(texts), len(vocab)))
    for r, t in enumerate(texts):
        for w in t.split():
            if w in index:
                M[r, index[w]] += 1
    return M


C = counts(docs)


def mnb_fit(C, y, alpha=1.0):
    classes = np.unique(y)
    prior = np.log(np.array([(y == c).mean() for c in classes]))
    word = np.array([C[y == c].sum(axis=0) for c in classes]) + alpha
    return classes, prior, np.log(word / word.sum(axis=1, keepdims=True))


from sklearn.naive_bayes import MultinomialNB

classes, prior, logw = mnb_fit(C, labels)
new = counts(["free money today", "project meeting at noon", "win lunch"])
scores = prior + new @ logw.T
ref = MultinomialNB(alpha=1.0).fit(C, labels)
print(classes[scores.argmax(axis=1)].tolist(), ref.predict(new).tolist())
print(np.allclose(logw, ref.feature_log_prob_))
print(len(vocab))
```

```text
[1, 0, 1] [1, 0, 1]
True
16
```

The classes of the three new texts and the word probabilities match
`MultinomialNB`. A text's score is the product of the counts matrix and the log
probabilities: a single matrix product. Many of the first spam filters rested
on this idea.

## What happens without smoothing?

```python
# almost no smoothing
classes0, prior0, logw0 = mnb_fit(C, labels, alpha=1e-12)
s0 = prior0 + counts(["win meeting"]) @ logw0.T
print(np.round(s0, 1).tolist())
```

```text
[[-32.9, -32.9]]
```

"win" appeared only in spam, "meeting" only in normal texts. Without smoothing
both classes collapse to −32.9 because of a word they never saw; the scores are
equal and the decision is meaningless. Laplace smoothing leaves an unseen word
a small but non-zero share.

## Summary

- Class = the largest `log P(class) + Σ log P(xᵢ | class)`; features are
  assumed independent within the class.
- Gaussian NB: a mean and variance per class; multinomial NB: word shares per
  class.
- Probabilities are not multiplied; their logarithms are added (underflow).
- Laplace smoothing (`alpha`) protects an unseen word from zeroing out.
- Learning is one counting pass; very fast and works with little data.
