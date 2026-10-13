Zipf's law said that text tables would be almost entirely zero. Let us
measure it:

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
X = CountVectorizer(ngram_range=(1, 2)).fit_transform(texts)
cells = X.shape[0] * X.shape[1]
print(X.shape, X.nnz, round(X.nnz / cells, 4))
dense_mb = cells * 8 / 1e6
sparse_mb = (X.data.nbytes + X.indices.nbytes + X.indptr.nbytes) / 1e6
print(round(dense_mb, 1), round(sparse_mb, 2))
```

```text
(2000, 2737) 52089 0.0095
43.8 0.63
```

- The table is 2000 rows × 2737 columns = 5.5 million cells; only 52,089 of
  them are non-zero (`nnz`, the number of non-zeros). **0.95% is filled.**
- Storing every cell would take 43.8 MB; scikit-learn stores only the
  non-zero values and their positions: 0.63 MB.

## How is a sparse matrix stored?

scikit-learn returns text tables in SciPy's **CSR** (compressed sparse row)
format. Three arrays:

| Array | What it holds |
|---|---|
| `data` | The non-zero values |
| `indices` | The column number of each value |
| `indptr` | Where each row starts inside `data` |

There are two practical reasons to know this:

1. **Do not call `X.toarray()`.** Turning a sparse matrix into a dense array
   writes every zero into memory; on big data you run out of memory.
2. **Choose models that work with sparse matrices.** Logistic regression,
   linear SVMs and Naive Bayes take sparse input directly; some models (for
   example many tree implementations) convert it to a dense array and slow
   down.

Selecting rows and columns works on sparse matrices too: `X[0]` is the first
document's row, `X[:, 5]` the fifth column. `X[0].nnz` gives how many
different n-grams appear in the first document.
