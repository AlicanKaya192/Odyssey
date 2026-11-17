`lora_forward(x, W, b, A, B, alpha)` should compute the LoRA layer's output:
`x · Wᵀ + b + (x · Aᵀ · Bᵀ) · alpha / r`. The rank `r` is the number of rows
of `A`. Return it as a nested list, every value with 3 places.

**Expected output:**

```
[[4.0, 2.0]]
```
