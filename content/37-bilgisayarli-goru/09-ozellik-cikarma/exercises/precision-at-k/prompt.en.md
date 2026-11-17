`precision_at_k(vectors, labels, k)` should average, over all vectors, the share
of each vector's `k` most similar neighbours (excluding itself) that have the
same label, rounded to 3 places.

**Expected output:**

```
1.0
0.8
```
