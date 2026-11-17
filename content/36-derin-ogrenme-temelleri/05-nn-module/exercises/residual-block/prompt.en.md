`Residual.forward` only gives the layer's output. Write the residual connection:
input + ReLU(the layer's output). `apply_block` sets the weights to 0.25 and the
bias to 0 and returns the result.

**Expected output:**

```
[1.0, -3.0]
[3.0, 3.0]
```
