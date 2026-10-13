`top_k_filter(probs, k)` should keep only the `k` most likely words (largest
first) and rescale their probabilities to sum to 1 (3 places).

**Expected output:**

```
2 order=0.625 parcel=0.375
1 order=1.0
```
