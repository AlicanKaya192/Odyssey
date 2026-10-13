`hybrid_best(lexical, semantic, alpha)` should return, for each query row, the
position of the document with the largest `alpha · lexical + (1 − alpha) ·
semantic` score.

**Expected output:**

```
0.0 [2, 1]
0.5 [1, 1]
1.0 [1, 0]
```
