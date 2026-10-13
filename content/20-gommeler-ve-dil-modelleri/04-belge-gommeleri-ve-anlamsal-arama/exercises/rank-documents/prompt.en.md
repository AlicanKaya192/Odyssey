`rank(doc_vectors, query)` should sort the documents by cosine similarity to the
query, largest first, and return their **positions** (indices). On equal
similarity the earlier document comes first.

**Expected output:**

```
[0, 1, 2, 3]
[2, 1, 0, 3]
```
