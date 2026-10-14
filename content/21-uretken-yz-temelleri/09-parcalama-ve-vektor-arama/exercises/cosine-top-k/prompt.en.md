`top_k(vectors, query, k)` should compute every vector's cosine similarity
with `query`: `a·b / (|a| |b|)`. Return the indices of the `k` most similar
vectors from highest to lowest; on a tie the smaller index first.

**Expected output:**

```
[1, 0]
[1]
```
