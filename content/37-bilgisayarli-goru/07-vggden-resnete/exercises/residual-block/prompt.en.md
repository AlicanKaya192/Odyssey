Write `ResidualBlock.forward`: `out = ReLU(bn1(conv1(x)))`,
`out = bn2(conv2(out))`, the result is `ReLU(out + x)`. The program also
checks that the block becomes `ReLU(x)` once `bn2`'s scale is zeroed: with
the residual path left, the block can pass the input through as it is.

**Expected output:**

```
(2, 4, 6, 6)
True
```
