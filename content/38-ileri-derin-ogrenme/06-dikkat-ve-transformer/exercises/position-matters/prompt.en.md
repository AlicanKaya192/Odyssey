The starter builds an encoder, a positional embedding (`pos`), an input `x`
and `perm`, which reverses the sequence. `position_matters(length)` should
return two values (inside `torch.no_grad()`, with `torch.allclose` and
`atol=1e-5`):

- `plain`: are `encoder(x)[:, perm]` and `encoder(x[:, perm])` the same?
- `positioned`: the same question, but with `x + pos.weight` and
  `x[:, perm] + pos.weight` given to the encoder.

**Expected output:**

```
[True, False]
[True, False]
```
