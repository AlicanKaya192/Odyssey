`masked_attention(X)` should return the weight table of self-attention that
takes `X` itself as query, key and value: scores `X @ X.T / √d`, `-inf`
above the diagonal, softmax on each row, 3 places.

**Expected output:**

```
[1.0, 0.0, 0.0]
[0.33, 0.67, 0.0]
[0.248, 0.248, 0.503]
```
