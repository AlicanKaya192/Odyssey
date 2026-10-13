How spread out are the weights? `attention_entropy(weights)` should compute the
entropy in bits: the sum of `-w · log2(w)` for every non-zero `w` (3
places). Attention on a single word should be 0, equal on four words 2
bits.

**Expected output:**

```
0.0
2.0
1.858
```
