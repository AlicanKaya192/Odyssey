PPMI has a known weakness: **rare context words** inflate PMI. If a context
word is rare, `P(c)` is small; appearing with it even once gives a large PMI.
A trick taken from Word2Vec's negative sampling distribution and applied to
PPMI (Levy, Goldberg and Dagan, 2015) softens this: when computing the
context probabilities, raise the counts to the power `α = 0.75`. Rare words
get a slightly larger share, `P(c)` does not stay as small, and PMI does not
inflate.

Let us compare three families of vectors on the lesson's analogy test: the
SVD of raw counts, the SVD of PPMI and the SVD of smoothed PPMI (all 20
dimensions).

```python
import numpy as np
from corpus_data import CAPITALS, GENDER_PAIRS, make_corpus

sentences = [s.split() for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                M[index[w], index[s[j]]] += 1


def ppmi(alpha):
    p_word = M.sum(axis=1) / M.sum()
    smooth = M.sum(axis=0) ** alpha
    p_context = smooth / smooth.sum()
    with np.errstate(divide="ignore"):
        P = np.log((M / M.sum()) / np.outer(p_word, p_context))
    return np.maximum(P, 0)


def vectors(X, k=20):
    U, S, _ = np.linalg.svd(X)
    E = U[:, :k] * S[:k]
    return E / np.linalg.norm(E, axis=1, keepdims=True)


def analogy(E, a, b, c):
    sims = E @ (E[index[b]] - E[index[a]] + E[index[c]])
    for w in (a, b, c):
        sims[index[w]] = -np.inf
    return vocab[int(np.argmax(sims))]


def score(E):
    gender = sum(analogy(E, m1, f1, m2) == f2 for m1, f1 in GENDER_PAIRS
                 for m2, f2 in GENDER_PAIRS if m1 != m2)
    caps = list(CAPITALS.items())
    capital = sum(analogy(E, c1, k1, c2) == k2 for c1, k1 in caps
                  for c2, k2 in caps if c1 != c2)
    return gender, capital


print("counts", score(vectors(M)))
print("ppmi", score(vectors(ppmi(1.0))))
print("ppmi 0.75", score(vectors(ppmi(0.75))))
```

```text
counts (27, 17)
ppmi (31, 24)
ppmi 0.75 (32, 25)
```

- The SVD of raw counts is the weakest: frequent words dominate the
  directions.
- PPMI is clearly better; smoothing adds one small step more.
- These differences were measured on small data and a test of 112
  questions; one or two right answers may be chance. In real studies the
  effect of smoothing was measured on large corpora and many tests. On your
  own data too, do not count a setting as an "improvement" without
  measuring.
