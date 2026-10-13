The distributional hypothesis says "similar context, similar meaning". But
what exactly is "similar meaning"? Let us look at adjectives:

```python
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
unit = M / np.linalg.norm(M, axis=1, keepdims=True)
for word in ["fast", "warm"]:
    sims = unit @ unit[index[word]]
    best = np.argsort(-sims)[1:4]
    print(word, [(vocab[i], round(float(sims[i]), 3)) for i in best])
```

```text
fast [('slow', 0.997), ('noisy', 0.993), ('new', 0.993)]
warm [('fresh', 0.999), ('sweet', 0.998), ('cold', 0.998)]
```

- The nearest neighbour of "fast" is "slow"; among the neighbours of "warm"
  is "cold", with 0.998 similarity. Words with opposite meanings appear **in
  the same contexts**: "the bus is fast" and "the bus is slow" follow the
  same pattern. Seen through their contexts, they can hardly be told apart.
- Distributional similarity means "can be used in the same place", not "means
  the same". It catches synonyms, antonyms and members of the same class
  ("cat", "dog") together.

## The price

- In sentiment analysis, if the vectors of "good" and "bad" are close, a
  model that looks only at vectors can mix them up. This is a known problem
  with real embeddings too; sentiment needs training on labelled data.
- If a word has several meanings ("bank": a money bank and a river bank), a
  single vector is the average of both. The **contextual** embeddings we meet
  at the end of this module get around this by giving a word a different
  vector depending on its sentence.
