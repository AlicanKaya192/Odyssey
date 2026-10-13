`rank(query)` should build a `TfidfVectorizer` on `DOCS`, transform the query
and return the documents' indices by cosine, largest first. Documents
scoring 0 must **not** be in the list. Use `np.argsort(...,
kind="stable")[::-1]` so ties keep their order.

**Expected output:**

```
[2, 3, 0]
[1]
[]
```
