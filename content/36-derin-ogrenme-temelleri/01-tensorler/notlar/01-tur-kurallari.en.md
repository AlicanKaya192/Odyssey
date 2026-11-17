The type (dtype) of a tensor operation's result is sometimes surprising. A
few examples with the lesson's `torch`:

```python
i = torch.tensor([1, 2, 3])
print((i / 2).dtype, (i // 2).tolist(), (i * 0.5).dtype)
print(torch.tensor([1, 2.5]).dtype, torch.tensor([True, False]).dtype)
try:
    i.mean()
except RuntimeError as error:
    print(str(error).split(".")[0])
print(i.float().mean().item())
```

```text
torch.float32 [0, 1, 1] torch.float32
torch.float32 torch.bool
mean(): could not infer output dtype
2.0
```

- `/` always gives a decimal result (`float32`); `//` is integer division
  and stays an integer.
- When integers and decimals mix, the result is decimal. If a list has a
  single decimal number, the whole tensor is `float32`.
- Comparisons (`>`, `==`) give a `bool` tensor.
- Averaging operations such as `mean` do not work on an integer tensor;
  call `.float()` first.

A short rule: everything that goes into the model is `float32`, class
labels are `int64`. If an error message says `Long`, read `int64`; `Float`
is `float32` and `Double` is `float64`.
