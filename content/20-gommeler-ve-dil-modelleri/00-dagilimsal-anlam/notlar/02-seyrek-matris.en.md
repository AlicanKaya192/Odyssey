In our small world the matrix is 166 × 166 = 27,556 cells. What happens with
a real language?

```python
from collections import Counter

from corpus_data import make_corpus
from scipy import sparse

sentences = [s.split() for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
pairs = Counter()
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                pairs[index[w], index[s[j]]] += 1
rows, cols = zip(*pairs)
M = sparse.csr_matrix((list(pairs.values()), (rows, cols)),
                      shape=(len(vocab), len(vocab)))
print(M.nnz, round(M.nnz / (M.shape[0] * M.shape[1]), 3))
dense_bytes = M.shape[0] * M.shape[1] * 8
sparse_bytes = M.data.nbytes + M.indices.nbytes + M.indptr.nbytes
print(dense_bytes, sparse_bytes)
print(round(100_000 ** 2 * 8 / 1e9), "GB")
```

```text
2306 0.084
220448 28340
80 GB
```

- Only about 8% of the cells are filled: most word pairs never appear
  together. A **sparse matrix** stores only the filled cells and their
  positions.
- Even in this small example the sparse form takes an eighth of the space of
  the dense form. The dense matrix of a 100,000-word vocabulary would be
  80 GB; because each word appears together with only a small part of the
  vocabulary, the share of filled cells is even lower in a real language.
- In NLP Fundamentals `CountVectorizer` returned a sparse matrix too, for the
  same reason. Counting pairs with `Counter` and handing them to
  `csr_matrix` is the usual way to build a co-occurrence matrix on a large
  corpus.
