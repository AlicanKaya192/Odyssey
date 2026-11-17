Once we have the gradient, we move the parameter in the direction that
lowers the loss: `w ← w − lr · gradient`. Writing this directly raises an
error:

```python
w = torch.tensor(5.0, requires_grad=True)
loss = (w - 2) ** 2
loss.backward()
try:
    w -= 0.1 * w.grad
except RuntimeError as error:
    print("in-place" in str(error))
with torch.no_grad():
    w -= 0.1 * w.grad
print(round(w.item(), 2), w.grad.item())
```

```text
True
4.4 6.0
```

- `w -= ...` is an in-place operation. PyTorch does not allow a leaf that
  wants a gradient to be changed in place; if this update were recorded, the
  next derivative would be wrong.
- Doing the update inside `torch.no_grad()` works: `5 − 0.1 · 6 = 4.4`. The
  derivative of the loss `(w − 2)²` is `2(w − 2) = 6`.
- `optimizer.step()` does exactly this inside. In the next section we repeat
  this update in a loop and train a model.
