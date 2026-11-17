`layer_norm(rows)` should normalise each **row** within itself: subtract the row's
mean, divide by `sqrt(variance + 1e-5)` (biased variance). Return the result as a
list of lists with 2 places. The solution should match `nn.LayerNorm`.

**Expected output:**

```
[[-1.22, 0.0, 1.22], [-0.71, -0.71, 1.41]]
```
