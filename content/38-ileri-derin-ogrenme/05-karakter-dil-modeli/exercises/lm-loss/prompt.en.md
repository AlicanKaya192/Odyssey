`lm_loss(logits, targets)`: `logits` is `(B, T, V)`, `targets` `(B, T)`.
Flatten them to `(B·T, V)` and `(B·T,)`, compute the loss with
`nn.functional.cross_entropy` and return it with 3 places.

**Expected output:**

```
1.386
0.0
```
