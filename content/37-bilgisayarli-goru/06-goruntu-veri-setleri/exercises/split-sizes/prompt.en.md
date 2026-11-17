`split_sizes(n, val_fraction, seed)` should split `range(n)` into training and
validation with `random_split`: validation has `int(n * val_fraction)`
examples, the generator is `torch.Generator().manual_seed(seed)`. Return
`[training size, validation size, the three smallest numbers in validation]`
(`val.indices`).

**Expected output:**

```
[48, 12, [5, 10, 13]]
[7, 3, [3, 4, 7]]
```
