The matrix `M` is ready. `similarity(a, b, drop)` should drop the **columns**
of the `drop` most frequent words (as contexts) and return the cosine
similarity between the two words' rows using the remaining columns, with 3
places. What happens to the similarity of "cat" and "bread" once the
frequent contexts are gone?

**Expected output:**

```
0 0.995 0.564
5 0.978 0.331
```
