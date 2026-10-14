`count_trainable(sizes, layers)` should return how many parameters are
updated in a network with layer sizes `sizes` (`[64, 32, 10]` → two layers)
if only the layers in `layers` are trained. Layer `i` has
`sizes[i] * sizes[i + 1] + sizes[i + 1]` parameters (weights and biases).

**Expected output:**

```
2410
330
```
