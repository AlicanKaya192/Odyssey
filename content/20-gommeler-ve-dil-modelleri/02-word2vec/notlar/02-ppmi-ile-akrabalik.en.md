Word2Vec seems not to count, but it does something very close to counting.
Levy and Goldberg (2014) showed that skip-gram with negative sampling moves,
by the end of training, towards the equality `v_word · u_context ≈
PMI(word, context) − log K` (K is the number of negative samples). So
Word2Vec indirectly writes a **shifted PMI matrix** as the product of two
small matrices, just as we wrote PPMI with SVD in the previous section.

Let us look with the lesson's trained `W_in` and `W_out`. On pairs seen
together at least 20 times we compare the dot product with `PMI − log 5`:

```python
X = W_in @ W_out.T
M = np.zeros((len(vocab), len(vocab)))
np.add.at(M, (pairs[:, 0], pairs[:, 1]), 1)
with np.errstate(divide="ignore"):
    pmi = np.log(M * M.sum() / np.outer(M.sum(axis=1), M.sum(axis=0)))
seen = M >= 20
shifted = pmi[seen] - np.log(5)
print(seen.sum(), round(float(np.corrcoef(X[seen], shifted)[0, 1]), 3))
print(round(float(X[seen].mean()), 2), round(float(shifted.mean()), 2))
```

```text
2076 0.865
0.13 0.2
```

- Over 2076 pairs the correlation is 0.865: the dot products largely follow
  the shifted PMI. Their means are close too (0.13 and 0.2).
- The equality is not exact: the model was trained for only five epochs, the
  vectors have 20 dimensions, and the equality is only expected after very
  long training with enough dimensions.
- The lesson: "counting" and "predicting" are not two separate worlds. Both
  compress a PMI matrix into a few dimensions; the differences are in the
  weighting, the training method and the settings. That is why a well-tuned
  PPMI + SVD comes close to Word2Vec on many tests.
