Write the function `backprop_w1(X, y, W1, b1, W2, b2)`: do the forward
pass (`tanh` hidden, sigmoid output), then `dz₂ = (p − y) / n`,
`dz₁ = (dz₂ W₂ᵀ) · (1 − H²)`, `dW₁ = Xᵀ dz₁`. Return `dW₁` with
`.round(4).tolist()`.

**Expected output:**

```
[0.0359, -0.1061]
[-0.0703, -0.0703]
```
