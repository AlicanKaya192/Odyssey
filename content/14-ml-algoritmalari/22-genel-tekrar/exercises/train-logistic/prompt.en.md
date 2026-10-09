Write the function `train_logistic(X, y, lr, epochs)`: start from `w = 0`,
`b = 0`; each epoch `p = σ(X w + b)`, `w ← w − lr · Xᵀ(p − y) / n`,
`b ← b − lr · mean(p − y)`. Return `(w list round(3), round(b, 3))`.

**Expected output:**

```
[-0.422, 5.887]
-2.517
```
