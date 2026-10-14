`nearest_labels(text, k)` should fit a `TfidfVectorizer` on the pool's
(`POOL`) texts, find the similarity scores as the dot product of the
pool's vectors and `text`'s vector, and return the categories of the `k`
most similar examples. Sort by score from largest to smallest; on equal
scores the one earlier in the pool comes first
(`sorted(range(len(POOL)), key=lambda i: -scores[i])`).

**Expected output:**

```
['shipping', 'shipping', 'refunds']
['returns', 'warranty']
```
