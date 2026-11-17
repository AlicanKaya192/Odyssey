`stack_vs_single(channels, n)` should return the total parameters of `n`
stacked 3 × 3 convolutions (`channels` → `channels`, with biases), the
parameters of a single convolution that sees the same receptive field, and
the side of that field, as `[stacked, single, field]`. The field of `n`
3 × 3 convolutions is `2n + 1`.

**Expected output:**

```
[73856, 102464, 5]
[27744, 50208, 7]
```
