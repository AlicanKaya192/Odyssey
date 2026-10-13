# Word Vectors with PPMI and SVD

In the previous section co-occurrence counts separated the classes of
meaning, but frequent words such as "the" dominated every vector: "cat" and
"bread" came out 0.612 similar. In this section we take two steps. First we
weight the counts with **PMI** and turn them into the question "how much
more often than expected?"; the effect of frequent words drops by itself.
Then we squeeze the 166-column vectors into 20 numbers with **SVD**. At the
end we have **dense word vectors** and can compute things like "king − man +
woman" with them.

## PMI: how much more often than expected?

"cat" and "the" appeared together 662 times, "cat" and "chased" 154 times.
But "the" is everywhere anyway. The real question: how much more often than
**chance would predict** do two words appear together? **Pointwise mutual
information** (PMI) measures this:

`PMI(w, c) = log( P(w, c) / (P(w) · P(c)) )`

If the two words were independent, the probability of seeing them together
would be `P(w) · P(c)`. PMI is the logarithm of the real probability divided
by that: 0 is "independent", positive "more often than expected", negative
"rarer than expected". It is the same idea as the PMI for word pairs you saw
in section 04 of NLP Fundamentals.

```python
from collections import Counter

import numpy as np
from corpus_data import make_corpus

sentences = [s.split() for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                M[index[w], index[s[j]]] += 1
total = M.sum()
p_word = M.sum(axis=1) / total
p_context = M.sum(axis=0) / total


def pmi(w, c):
    joint = M[index[w], index[c]] / total
    return np.log(joint / (p_word[index[w]] * p_context[index[c]]))


with np.errstate(divide="ignore"):
    for w, c in [("cat", "chased"), ("cat", "the"), ("cat", "cooked")]:
        print(w, c, int(M[index[w], index[c]]), round(float(pmi(w, c)), 2))
```

```text
cat chased 154 2.33
cat the 662 0.75
cat cooked 0 -inf
```

- "cat" and "the" appeared 662 times, but their PMI is only 0.75: "the" is
  next to every word, so this pairing says little.
- "cat" and "chased" appeared less often (154), but the PMI is 2.33: about
  ten times chance (`e^2.33 ≈ 10`).
- A pair never seen together has a PMI of minus infinity (`log 0`). To work
  with the numbers we will fix this.

## The PPMI matrix

**Positive PMI** (PPMI) sets negative values, infinity included, to 0:
`PPMI = max(PMI, 0)`. Negative PMI is unreliable: saying "rarer than
expected" needs a great deal of data. Let us compute the whole matrix at
once:

```python
with np.errstate(divide="ignore"):
    P = np.log((M / total) / np.outer(p_word, p_context))
P = np.maximum(P, 0)


def cosine(X, a, b):
    x, y = X[index[a]], X[index[b]]
    return round(float(x @ y / np.linalg.norm(x) / np.linalg.norm(y)), 3)


def neighbours(X, word, k=4):
    unit = X / np.linalg.norm(X, axis=1, keepdims=True)
    sims = unit @ unit[index[word]]
    return [vocab[i] for i in np.argsort(-sims)[1:k + 1]]


print(cosine(P, "cat", "dog"), cosine(P, "cat", "bread"))
for word in ["cat", "king", "paris"]:
    print(word, neighbours(P, word))
```

```text
0.995 0.033
cat ['cow', 'dog', 'rabbit', 'horse']
king ['queen', 'uncle', 'brother', 'man']
paris ['athens', 'vienna', 'berlin', 'rome']
```

- "cat" and "dog" stayed 0.995 similar, but "cat" and "bread" fell from
  0.612 to 0.033. Shared frequent words no longer create similarity; the
  separation is much sharper.
- `np.outer(p_word, p_context)` gives the expected probability under
  independence for every cell; the division and the logarithm are applied to
  the whole matrix at once.

## Shortening with SVD

The PPMI vectors are still 166 numbers long and mostly 0. A real language
would have hundreds of thousands of columns. **SVD** (singular value
decomposition) writes the matrix as `U · diag(S) · Vᵀ`; the singular values
(`S`) are sorted from largest to smallest. Keeping the first k and dropping
the rest keeps the k directions of the matrix that carry the most
information. (SVD is behind the PCA of the ML Algorithms module too.)

```python
U, S, Vt = np.linalg.svd(P)
energy = (S ** 2).cumsum() / (S ** 2).sum()
print([round(float(energy[k - 1]), 3) for k in [5, 10, 20, 50]])
k = 20
E = U[:, :k] * S[:k]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
print(E.shape)
for word in ["cat", "bread", "car"]:
    print(word, neighbours(E, word))
```

```text
[0.378, 0.593, 0.794, 0.948]
(166, 20)
cat ['cow', 'rabbit', 'mouse', 'horse']
bread ['rice', 'soup', 'cake', 'cheese']
car ['truck', 'tram', 'bus', 'bike']
```

- 20 dimensions keep 79.4% of the matrix's "energy" (the sum of the squared
  singular values). Each word is now a **dense** vector of 20 numbers.
- The neighbours stayed the same: animals, foods, vehicles. The information
  was squeezed from 166 columns into 20, but the classes of meaning were
  kept.
- We scaled the vectors to unit length, so the dot product is the cosine
  similarity directly.

## Analogies

In dense vectors a difference can carry a **direction**: if the difference
between "king" and "queen" is like the difference between "man" and
"woman", then `king − man + woman` lands near "queen".

```python
from corpus_data import CAPITALS, GENDER_PAIRS


def analogy(E, a, b, c):
    """a : b :: c : ?  →  b - a + c vektörüne en yakın kelime."""
    target = E[index[b]] - E[index[a]] + E[index[c]]
    sims = E @ target
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


print(analogy(E, "man", "king", "woman"))
print(analogy(E, "paris", "france", "rome"))
print(score(E), len(GENDER_PAIRS) * 7, len(CAPITALS) * 7)
```

```text
queen
italy
(31, 24) 56 56
```

- `king − man + woman` → "queen", `france − paris + rome` → "italy". Nobody
  said "a queen is a female king" or "Rome is the capital of Italy"; these
  relations came out of co-occurrence counts alone.
- But not always: 31 of 56 gender analogies and 24 of 56 capital analogies
  are right. The analogy test is the classic measure of embeddings, and real
  embeddings are not perfect at it either.
- We kept the three words of the question out of the candidates; otherwise
  the nearest word is often one of them.

## How many dimensions?

```python
for k in [2, 5, 10, 20, 50, 166]:
    Ek = U[:, :k] * S[:k]
    Ek = Ek / np.linalg.norm(Ek, axis=1, keepdims=True)
    print(k, score(Ek), analogy(Ek, "man", "king", "woman"))
```

```text
2 (12, 3) his
5 (27, 9) queen
10 (31, 23) queen
20 (31, 24) queen
50 (32, 18) queen
166 (32, 8) queen
```

- 2 dimensions are too few: even "king − man + woman" gives "his".
- Capital analogies are best at 20 dimensions (24) and **fall** as the
  dimension grows: at 166, with no shortening at all, only 8. Cutting also
  drops noise; a few strong directions carry the relation more cleanly.
- The dimension is a setting: real embeddings usually use between 100 and
  300, chosen by measuring on a task.

## Summary

- PMI measures how much more often than chance a pairing is; it lowers the
  weight of frequent words by itself. PPMI sets negatives to 0.
- With PPMI the similarity of "cat" and "bread" fell from 0.612 to 0.033.
- SVD squeezes the PPMI matrix into a few dense dimensions; 20 dimensions
  kept 79% of the information and preserved the classes of meaning.
- In dense vectors differences carry directions: `king − man + woman ≈
  queen`. Shortening improved the analogies; the dimension is chosen by
  measuring.
