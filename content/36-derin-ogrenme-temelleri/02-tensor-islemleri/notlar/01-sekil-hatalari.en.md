The most common error in deep learning is a shape error. When the inner
dimensions of a matrix product do not match, PyTorch prints both shapes:

```python
x = torch.ones(4, 3)
w = torch.ones(4, 2)
try:
    x @ w
except RuntimeError as error:
    print(error)
print((x @ w[:3]).shape, (x @ torch.ones(3)).shape)
```

```text
mm: mat1 and mat2 shapes cannot be multiplied (4x3 and 4x2)
torch.Size([4, 2]) torch.Size([4])
```

- `4x3` and `4x2`: the left one's column count (3) does not equal the right
  one's row count (4). A product only works as `(a, b) @ (b, c)`.
- `w[:3]` takes the first three rows and makes `(3, 2)`; the product is
  `(4, 2)`.
- If the right side is a one-dimensional vector (`(3,)`), the result is
  one-dimensional too: `(4,)`.

When you see a shape error, the first thing to do is print the `shape` of
the tensors involved just before the error. We come back to this in the
Debugging section.
