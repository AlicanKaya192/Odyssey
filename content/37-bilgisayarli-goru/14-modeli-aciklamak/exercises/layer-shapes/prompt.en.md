`layer_shapes(size)` should attach a forward hook to every layer of the given
`model`, run the model on `torch.zeros(1, 1, size, size)` and return the
output shape of each layer as lists (in order). The hooks must be removed
when done: the function must give the same result when called a second
time.

**Expected output:**

```
[1, 4, 8, 8]
[1, 4, 8, 8]
[1, 4, 4, 4]
[1, 8, 2, 2]
[1, 8, 2, 2]
[1, 32]
[1, 128]
6
```
