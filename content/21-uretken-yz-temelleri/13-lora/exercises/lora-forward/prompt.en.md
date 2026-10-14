`lora_forward(x, W, A, B)` should return the layer's output with the frozen
`W` and the LoRA correction: `x @ W + (x @ A) @ B`. The result is a nested
list with every number rounded to 3 places. (It gives the same result as
`x @ (W + A @ B)`; for a large layer `(x @ A) @ B` is cheaper.)

**Expected output:**

```
[[1.0, 3.0]]
```
