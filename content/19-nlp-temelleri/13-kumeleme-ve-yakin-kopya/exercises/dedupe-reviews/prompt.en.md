`dedupe(n, threshold)` should walk the first `n` reviews in order. A review is
dropped if its Jaccard similarity with any review **already kept** is
`threshold` or more; otherwise it is kept. Return the number of reviews
kept. `shingles` and `jaccard` are ready.

**Expected output:**

```
591
589
```
