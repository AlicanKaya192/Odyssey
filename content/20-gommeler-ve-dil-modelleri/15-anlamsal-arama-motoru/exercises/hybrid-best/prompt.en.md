`hybrid_best(lexical, semantic, alpha)` should compute the score `alpha · lexical
+ (1 − alpha) · semantic` for each article (3 places) and return `[the best
article's index, its score]` (the first one on ties).

**Expected output:**

```
0.0 [0, 0.9]
0.3 [0, 0.63]
1.0 [1, 0.6]
```
