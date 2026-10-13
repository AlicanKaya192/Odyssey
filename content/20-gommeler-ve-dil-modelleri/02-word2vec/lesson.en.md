# Word2Vec

PPMI and SVD were based on **counting**: first count every co-occurrence,
then compress the matrix. In 2013 **Word2Vec** by Mikolov and colleagues
opened another way: learning the vectors **by predicting**. Build a small
model that looks at a word and tries to predict the words around it; let the
model's weights be the word vectors. In this section we write the most common
form of Word2Vec, **skip-gram with negative sampling** (SGNS), from scratch
with NumPy, train it and compare it with PPMI + SVD.

## Training pairs

Skip-gram takes each word as the **centre** and builds a (centre, context)
pair with every word in its window. The model will try to predict the
context from the centre.

```python
from collections import Counter

import numpy as np
from corpus_data import make_corpus

sentences = [s.split() for s in make_corpus(20000)]
counts = Counter(w for s in sentences for w in s)
vocab = sorted(counts)
index = {w: i for i, w in enumerate(vocab)}


def skipgram_pairs(tokens, window=2):
    return [(tokens[i], tokens[j]) for i in range(len(tokens))
            for j in range(max(0, i - window), min(len(tokens), i + window + 1))
            if j != i]


print(skipgram_pairs("the cat chased the dog".split())[:4])
pairs = np.array([(index[a], index[b]) for s in sentences
                  for a, b in skipgram_pairs(s)])
print(pairs.shape)
```

```text
[('the', 'cat'), ('the', 'chased'), ('cat', 'the'), ('cat', 'chased')]
(321232, 2)
```

20,000 sentences give 321,232 pairs. Instead of counting a co-occurrence
matrix, we show these pairs to the model one batch at a time.

## The model: two tables and a probability

Each word has **two** vectors: the `W_in` row used when it is the centre and
the `W_out` row used when it is the context. The probability that a (centre,
context) pair is a "real pair" is the **sigmoid** of the dot product of the
two vectors:

`P(real | centre, context) = σ(v_centre · u_context)`, `σ(x) = 1 / (1 + e^-x)`

```python
dim = 20
rng = np.random.default_rng(0)
W_in = (rng.random((len(vocab), dim)) - 0.5) / dim
W_out = np.zeros((len(vocab), dim))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


v, u = W_in[index["cat"]], W_out[index["chased"]]
print(W_in.shape, W_out.shape)
print(sigmoid(v @ u))
```

```text
(166, 20) (166, 20)
0.5
```

- `W_in` starts with small random numbers, `W_out` with zeros (as in
  Word2Vec's own code). At the start every pair has probability exactly 0.5:
  the model knows nothing.
- Training will adjust the vectors to push the probability of real pairs
  towards 1. At the end the rows of `W_in` are our word vectors.

## Negative sampling

If we show only real pairs, the model "wins" by making every probability 1.
It has to see **wrong** pairs too: for each real pair we draw K random words
from the vocabulary (here 5) and say "these are not context". The random
words are drawn by frequency, but with the counts raised to the power 0.75;
so "the" is picked a little less and rare words a little more (the smoothing
from the previous section's note).

```python
freq = np.array([counts[w] for w in vocab], dtype=float)
noise = freq ** 0.75 / (freq ** 0.75).sum()
for word in ["the", "cat", "throne"]:
    share = counts[word] / freq.sum()
    print(word, round(share, 4), round(float(noise[index[word]]), 4))
```

```text
the 0.2039 0.0958
cat 0.0053 0.0062
throne 0.0014 0.0022
```

"the" is 20.4% of the tokens but 9.6% of the negative samples; "throne" rises
from 1.4 to 2.2 per thousand. The loss function:

`L = −log σ(v · u_context) − Σ log σ(−v · u_negative)`

The first term wants to raise the probability of the real pair, the second
to lower the probability of the random pairs.

## Training

The derivative of the loss is simple: for the real pair the derivative of the
score is `σ(s) − 1`, for a negative pair `σ(s)`. We process the pairs in
batches of 256 and in each batch move the three tables a little against the
derivative (gradient descent; section 04 of ML Algorithms). The learning rate
decreases linearly during training.

```python
def train(dim=20, negatives=5, epochs=5, lr=0.05, batch=256, seed=0):
    rng = np.random.default_rng(seed)
    W_in = (rng.random((len(vocab), dim)) - 0.5) / dim
    W_out = np.zeros((len(vocab), dim))
    losses = []
    for epoch in range(epochs):
        step = lr * (1 - epoch / epochs)
        order = rng.permutation(len(pairs))
        total = 0.0
        for start in range(0, len(pairs), batch):
            c, o = pairs[order[start:start + batch]].T
            neg = rng.choice(len(vocab), size=(len(c), negatives), p=noise)
            v, u_pos, u_neg = W_in[c], W_out[o], W_out[neg]
            s_pos = sigmoid((v * u_pos).sum(axis=1))
            s_neg = sigmoid(np.einsum("bkd,bd->bk", u_neg, v))
            total -= np.log(s_pos).sum() + np.log(1 - s_neg).sum()
            g_pos, g_neg = (s_pos - 1)[:, None], s_neg[:, :, None]
            grad_v = g_pos * u_pos + (g_neg * u_neg).sum(axis=1)
            np.add.at(W_out, o, -step * g_pos * v)
            np.add.at(W_out, neg, -step * g_neg * v[:, None, :])
            np.add.at(W_in, c, -step * grad_v)
        losses.append(round(float(total / len(pairs)), 3))
    return W_in, W_out, losses


W_in, W_out, losses = train()
print(losses)
```

```text
[2.351, 1.985, 1.756, 1.565, 1.438]
```

- The loss falls every epoch: the model learns to tell real pairs from
  random ones.
- `np.add.at` is needed: the same word can appear several times in a batch
  (especially "the"); writing `W_in[c] -= ...` would keep only one of the
  updates for repeated rows.
- `einsum("bkd,bd->bk", ...)` takes the dot products of each pair's K
  negative vectors with the centre vector in one go.

## The result

```python
def unit(W):
    return W / np.linalg.norm(W, axis=1, keepdims=True)


def neighbours(E, word, k=4):
    sims = E @ E[index[word]]
    return [vocab[i] for i in np.argsort(-sims)[1:k + 1]]


def analogy(E, a, b, c):
    sims = E @ (E[index[b]] - E[index[a]] + E[index[c]])
    for w in (a, b, c):
        sims[index[w]] = -np.inf
    return vocab[int(np.argmax(sims))]


E = unit(W_in)
for word in ["cat", "bread", "paris"]:
    print(word, neighbours(E, word))
print(analogy(E, "man", "king", "woman"), analogy(E, "paris", "france", "rome"))
```

```text
cat ['sheep', 'mouse', 'dog', 'cow']
bread ['cake', 'soup', 'cheese', 'rice']
paris ['lisbon', 'athens', 'berlin', 'vienna']
queen italy
```

- The neighbours are class by class again, and `king − man + woman` is
  "queen" again. This time we counted no matrix; the vectors emerged while
  trying to predict pairs.
- `france − paris + rome` is "italy" too. But a single example can mislead;
  in the next block we look at the whole test.

## Both tables together

We dropped `W_out`; but it is a table of word vectors too. A habit of Word2Vec
users is to add the two tables. Let us try it on the analogy test:

```python
from corpus_data import CAPITALS, GENDER_PAIRS


def score(E):
    gender = sum(analogy(E, m1, f1, m2) == f2 for m1, f1 in GENDER_PAIRS
                 for m2, f2 in GENDER_PAIRS if m1 != m2)
    caps = list(CAPITALS.items())
    capital = sum(analogy(E, c1, k1, c2) == k2 for c1, k1 in caps
                  for c2, k2 in caps if c1 != c2)
    return gender, capital


print("W_in", score(unit(W_in)))
print("W_in + W_out", score(unit(W_in + W_out)))
```

```text
W_in (28, 5)
W_in + W_out (29, 56)
```

- `W_in` alone is weak on capitals: 5 of 56 (PPMI + SVD found 24). The two
  tables together find all 56 of 56.
- Why? Similarity in `W_in` is "appearing in the same contexts": "paris" and
  "rome" are alike. `W_out` holds how a word looks **as a context**; the
  product of `W_in` and `W_out` means "appearing together": "paris" and
  "france". The sum combines both kinds, and the capital relation is exactly
  the relation of two words that "appear together".
- Remember this was measured in a small world; with real embeddings the
  effect of the sum is smaller. But which table counts as "the word vectors"
  is also a choice, and worth measuring.

## Summary

- Word2Vec learns vectors not by counting but by predicting the context from
  the centre word. Skip-gram turns every (centre, context) pair into an
  example.
- Negative sampling adds K random "wrong" pairs to every real pair; the
  random words are drawn by frequency to the power 0.75.
- Training is a sigmoid and gradient descent: the loss fell from 2.351 to
  1.438. `np.add.at` for repeated rows.
- The neighbours and `king − man + woman = queen` came out as with the
  counting method. `W_in + W_out` found every capital analogy.
