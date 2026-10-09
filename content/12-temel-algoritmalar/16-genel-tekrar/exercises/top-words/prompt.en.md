Write the function `top_words(words, k)`: it returns the `k` most frequent
words as a list, **by count descending**, and **alphabetically** when the
counts are equal.

Two steps: count with a dictionary, then sort or use a heap
(`heapq.nsmallest(k, ..., key=...)`). For the key, a `(-count, word)` tuple
gives both criteria at once. No `Counter` and no `most_common`.

**Expected output:**

```
['the', 'and', 'cat']
['a', 'b']
```
