`SquaresDataset(n)` should give the pair `(x, x²)` for each `i` from `0` to
`n − 1`: both one-element decimal tensors (`torch.tensor([float(i)])`). Write the
`__len__` and `__getitem__` methods of the class.

**Expected output:**

```
[5, 3.0, 9.0]
[10, 0.0, 0.0]
```
