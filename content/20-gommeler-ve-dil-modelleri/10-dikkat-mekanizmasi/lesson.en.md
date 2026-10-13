# The Attention Mechanism

An RNN carries information step by step: to remember a subject three words
back, the information has to be written into and read from the hidden state
three times, and some of it is lost at each step. The **attention
mechanism** offers another way: when deciding on the next word, **look
directly at all the previous words** and learn how important each one is.
Distance no longer matters; every word is reachable in a single step. The
idea appeared in machine translation in 2014 (Bahdanau and colleagues) and
became the basis of the transformer. In this section we first understand
attention with a small example, then build an attention model that learns.

## A soft dictionary lookup

In a Python dictionary a key reaches exactly one value. Attention is the
**soft** version: a **query** is compared with all the **keys**, the
similarities are turned into weights with softmax, and the weighted average
of the **values** is taken.

```python
import numpy as np


def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


keys = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])
values = np.array([[10.0], [20.0], [30.0]])
query = np.array([1.0, 0.2])
scores = keys @ query / np.sqrt(len(query))
weights = softmax(scores)
print(scores.round(3), weights.round(3))
print((weights @ values).round(2))
```

```text
[0.707 0.141 0.594] [0.406 0.231 0.363]
[19.57]
```

- The query is most similar to the first key, which gets the largest weight,
  but the other two get a share too. The result is a mix of the values.
- Everything is differentiable: the query, the keys and the values can be
  learned. A hard "pick the best" decision would not be differentiable.

## Why divide by √d?

We divided the scores by the square root of the vector size. What if we did
not? For random vectors the size of the dot product grows with the
dimension:

```python
rng = np.random.default_rng(0)
for d in [4, 64, 512]:
    q = rng.normal(size=(1000, d))
    k = rng.normal(size=(1000, 10, d))
    s = np.einsum("nd,nkd->nk", q, k)
    raw = softmax(s).max(axis=1).mean()
    scaled = softmax(s / np.sqrt(d)).max(axis=1).mean()
    print(d, round(float(s.std()), 1), round(float(raw), 3), round(float(scaled), 3))
```

```text
4 2.0 0.493 0.305
64 7.9 0.875 0.322
512 22.8 0.952 0.322
```

- At 512 dimensions the standard deviation of the scores is 22.8: softmax
  gives almost all the weight to a single key (the average largest weight is
  0.952). The derivatives of such a "hard" softmax are tiny, and learning
  stops.
- Dividing by `√d` brings the scores to the same scale at every dimension:
  the largest weight stays around 0.32. The name of the transformer's
  "scaled dot-product attention" comes from this.

## An attention model that learns

Now let us see attention solve the distance problem. The task: take the part
of a sentence up to a pronoun and predict whether the coming pronoun is male
("he", "his") or female ("she", "her"). In "the queen smiled and ___" the
answer is three words back.

```python
from corpus_data import GENDER_PAIRS, make_corpus

examples = []
for sentence in make_corpus(20000):
    words = sentence.split()
    for i, w in enumerate(words):
        if w in {"he", "his", "she", "her"} and i >= 2:
            examples.append((words[:i], int(w in {"she", "her"})))
vocab = sorted({w for prefix, _ in examples for w in prefix})
index = {w: i for i, w in enumerate(vocab)}
print(len(examples), examples[0])
```

```text
2257 (['the', 'prince', 'played', 'with'], 0)
```

The model is very simple: an embedding for each word (`E`), a single learned
**query** vector (`q`) and an output layer. The query stands for the question
"which word tells the gender?"; each word's embedding is both key and value.

```python
rng = np.random.default_rng(0)
E = rng.normal(0, 0.1, (len(vocab), 16))
q = rng.normal(0, 0.1, 16)
w, b = np.zeros(16), 0.0


def attend(prefix):
    X = E[[index[t] for t in prefix]]
    a = softmax(X @ q)
    c = a @ X
    p = 1 / (1 + np.exp(-(w @ c + b)))
    return X, a, c, p


for epoch in range(3):
    total = 0.0
    for i in rng.permutation(len(examples)):
        prefix, y = examples[i]
        X, a, c, p = attend(prefix)
        total -= np.log(p if y else 1 - p)
        dz = p - y
        dc = dz * w
        da = X @ dc
        ds = a * (da - a @ da)
        dX = np.outer(a, dc) + np.outer(ds, q)
        w, b, q = w - 0.5 * dz * c, b - 0.5 * dz, q - 0.5 * ds @ X
        np.add.at(E, [index[t] for t in prefix], -0.5 * dX)
    print(epoch, round(float(total / len(examples)), 3))
```

```text
0 0.05
1 0.0
2 0.0
```

The backward pass has only one new piece compared with the network of 08:
the derivative of softmax, `a · (da − a · da)`. The loss falls almost to zero
in the first epoch.

## Where does the model look?

```python
correct = 0
for male, female in GENDER_PAIRS:
    for word, y in [(male, 0), (female, 1)]:
        correct += (attend(["the", word, "smiled", "and"])[3] > 0.5) == y
print(correct, 2 * len(GENDER_PAIRS))
for prefix in [["the", "queen", "smiled", "and"], ["the", "boy", "smiled", "and"]]:
    _, a, _, p = attend(prefix)
    print(" ".join(f"{t}:{x:.2f}" for t, x in zip(prefix, a)), round(float(p), 2))
```

```text
16 16
the:0.00 queen:0.99 smiled:0.00 and:0.00 1.0
the:0.11 boy:0.42 smiled:0.24 and:0.22 0.0
```

- The pronoun is right for 16 of 16 person words. Distance does not matter:
  attention looks at "queen" from three words away in a single step.
- In "the queen smiled and" 0.99 of the weight is on "queen". Without being
  told, the model learned to look at the word carrying the gender.
- In "the boy smiled and" the weight is more spread out but the decision is
  still right: male words behave like a "default" here. Attention weights do
  not always fully explain the model's decision (the first note).

## Summary

- Attention is a soft dictionary lookup: the query is compared with the
  keys, and the softmax weights mix the values.
- Scores are divided by `√d`; otherwise at large dimensions softmax becomes
  hard and learning stops.
- Attention reaches every word in a single step; for long-range dependencies
  there is no need to carry information step by step.
- A small learning attention model scored 16/16 on the pronoun test and put
  its weight on the word carrying the gender.
