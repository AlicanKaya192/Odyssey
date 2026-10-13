In a plain average every word counts equally. The **SIF** (smooth inverse
frequency) method of Arora and colleagues (2017) gives frequent words less
weight: a word's weight is `a / (a + p(w))`, `p(w)` the word's frequency, `a`
a small constant (here 0.001). Let us try it with the lesson's `E`,
`counts`, `vocab` and search setup:

```python
total = sum(counts.values())
weight = {w: 1e-3 / (1e-3 + counts[w] / total) for w in vocab}


def embed_weighted(text):
    words = [w for w in TOKEN.findall(text.lower())
             if w in index and w not in ENGLISH_STOP_WORDS]
    if not words:
        return np.zeros(E.shape[1])
    v = np.sum([weight[w] * E[index[w]] for w in words], axis=0)
    return v / np.linalg.norm(v)


A_w = np.array([embed_weighted(t) for t in article_texts])
Q_w = np.array([embed_weighted(q) for q in queries])
hits = categories[(Q_w @ A_w.T).argmax(axis=1)] == labels
print(round(float(hits.mean()), 3))
print([round(weight[w], 3) for w in ["the", "refund", "pracel"]])
```

```text
0.791
[0.016, 0.165, 0.963]
```

- The weighted average is **worse** here than the plain average (81.9%).
  Since we had already dropped stop words, the frequent-word problem was
  largely solved; SIF instead brings forward rare words, here mostly
  **typos** ("pracel" weighs more than "refund").
- In the original SIF work a common direction of all sentence vectors (the
  first singular vector) is also removed; here we tried only the weighting.
- The lesson again: a method that worked somewhere does not work everywhere.
  Measure on your own data.
