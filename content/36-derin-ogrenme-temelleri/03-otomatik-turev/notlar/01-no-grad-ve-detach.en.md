Sometimes we do not want a computation to enter the graph: when predicting,
when printing a value, or when moving to NumPy. There are two tools:

```python
w = torch.tensor(3.0, requires_grad=True)
with torch.no_grad():
    doubled = w * 2
print(doubled.requires_grad, (w * 2).requires_grad)
d = w.detach()
print(d.requires_grad, d.item())
try:
    w.numpy()
except RuntimeError as error:
    print(str(error).split(".")[0])
print(w.detach().numpy())
```

```text
False True
False 3.0
Can't call numpy() on Tensor that requires grad
3.0
```

- No operation inside a `torch.no_grad()` block is recorded. It is used in
  prediction and evaluation code; it saves memory and time.
- `detach()` gives a tensor that shows the same data but is cut off from the
  graph.
- A tensor that wants a gradient cannot be turned into NumPy directly; the
  error message even gives the fix: `detach()` first.

When recording a loss value, write `loss.item()`; do not collect `loss`
itself in a list: the tensor keeps its graph alongside it and memory grows
for nothing.
