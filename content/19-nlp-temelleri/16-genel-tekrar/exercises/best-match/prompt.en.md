`best_match(query, docs)` should lowercase the query and each document, split
them on spaces, compute the **cosine similarity** of their word counts
(`Counter`) and return the index of the most similar document. On ties the
first document wins; a zero-length vector has similarity 0.

**Expected output:**

```
1
2
```
