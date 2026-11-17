In PyTorch code you often see `view` next to `reshape`. Both change the
shape; the difference is in how the data sits in memory:

```python
m = torch.arange(6).reshape(2, 3)
print(m.view(3, 2).shape)
mt = m.T
print(mt.shape, mt.is_contiguous())
try:
    mt.view(6)
except RuntimeError as error:
    print("reshape" in str(error))
print(mt.reshape(6).tolist())
```

```text
torch.Size([3, 2])
torch.Size([3, 2]) False
True
[0, 3, 1, 4, 2, 5]
```

- `view` does not make a copy; it looks at the same memory in another
  shape. For that, the elements must sit in order in memory (contiguous).
- `m.T` (the transpose) swaps rows and columns but does not move the
  memory; the order breaks and `view` raises an error. The error message
  itself suggests using `reshape`.
- `reshape` copies if it has to and behaves like `view` otherwise. When
  unsure, write `reshape`.
