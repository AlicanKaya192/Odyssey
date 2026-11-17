Methods whose names end with an underscore (`add_`, `mul_`, `zero_`) change
a tensor **in place**: they build no new tensor but write into the old one.

```python
a = torch.tensor([1.0, 2.0])
b = a
a.add_(10)
print(a.tolist(), b.tolist())
c = a
a = a + 1
print(a.tolist(), c.tolist())
```

```text
[11.0, 12.0] [11.0, 12.0]
[12.0, 13.0] [11.0, 12.0]
```

- `b = a` is not a copy but a second name for the same tensor.
  `a.add_(10)` changes both.
- `a = a + 1` builds a new tensor and gives it the name `a`; `c` stays on
  the old tensor.
- In-place operations save memory but need care. Automatic differentiation
  raises an error when it notices that a value it kept for backpropagation
  was changed in place. In your own code, if unsure, use the `a = a + 1`
  form; library-internal in-place operations such as
  `optimizer.zero_grad()` are safe.
