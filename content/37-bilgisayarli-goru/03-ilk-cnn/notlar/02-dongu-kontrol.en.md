If training behaves unexpectedly, look at this list first:

| Symptom | Common cause |
|---|---|
| The loss never falls | `optimizer.step()` forgotten, or the optimizer was given another model's parameters |
| The loss falls, then swings wildly | `zero_grad()` forgotten: gradients pile up |
| The starting loss is far above `log(number of classes)` | A softmax after the last layer (`CrossEntropyLoss` wants raw scores) |
| The test accuracy differs a little on each measurement | `model.eval()` forgotten |
| A label type error | The labels are `float`; `CrossEntropyLoss` wants `int64` |

The cause of the second row is that PyTorch **adds** gradients on top:

```python
import torch

w = torch.tensor([2.0], requires_grad=True)
loss = (w * 3).sum()
loss.backward()
print(w.grad.item())
loss = (w * 3).sum()
loss.backward()
print(w.grad.item())
w.grad.zero_()
print(w.grad.item())
```

```text
3.0
6.0
0.0
```

The second `backward` raised the gradient from 3 to 6: the new gradient was
added on top of the old one. `optimizer.zero_grad()` in every batch clears
this build-up. (The behaviour is deliberate: when memory runs short it is used
to add up the gradients of several small batches and take a single step.)
