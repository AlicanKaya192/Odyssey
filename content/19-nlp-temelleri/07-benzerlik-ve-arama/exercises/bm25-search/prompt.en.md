`bm25(query)` should compute the BM25 score for every article and return a list.
For every query word `w` that appears in the article:

- `idf = log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))`
- `norm = k1 * (1 - b + b * len(doc) / avg_len)`
- add `idf * tf[w] * (k1 + 1) / (tf[w] + norm)` to the score

`tokens`, `df`, `avg_len`, `N` and `analyze` are ready.

**Expected output:**

```
9.441
Tracking your order
4.565
Resetting your password
```
