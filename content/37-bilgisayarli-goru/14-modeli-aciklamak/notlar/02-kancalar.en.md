Hooks are the way to look inside a network without touching its code, but if
they are not removed they quietly pile up. Running the same notebook cell
twice attaches the hook twice.

```python
import torch
from torch import nn

layer = nn.Linear(2, 2)
calls = []
for _ in range(3):
    layer.register_forward_hook(lambda module, inputs, output: calls.append(1))
layer(torch.zeros(1, 2))
print(len(layer._forward_hooks), len(calls))
```

```text
3 3
```

The hook attached three times was called three times in a single forward
pass. The right way is to keep the handle and remove it when the work is
done; `try` / `finally` makes sure it is removed even if an error occurs:

```python
def output_shapes(model, x):
    shapes = []
    handles = [part.register_forward_hook(
        lambda module, inputs, output: shapes.append(tuple(output.shape)))
        for part in model]
    try:
        model(x)
    finally:
        for handle in handles:
            handle.remove()
    return shapes


net = nn.Sequential(
    nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten()
)
print(output_shapes(net, torch.zeros(1, 1, 8, 8)))
print(output_shapes(net, torch.zeros(1, 1, 8, 8)))
print([len(part._forward_hooks) for part in net])
```

```text
[(1, 4, 8, 8), (1, 4, 8, 8), (1, 4, 4, 4), (1, 64)]
[(1, 4, 8, 8), (1, 4, 8, 8), (1, 4, 4, 4), (1, 64)]
[0, 0, 0, 0]
```

- Four layers, four shapes in both calls: the hooks were removed each time.
- There are hooks in the backward direction too: `register_full_backward_hook`
  gives the gradient passing through a layer. Asking for the gradient
  directly with `torch.autograd.grad`, as in the lesson, is often simpler.
- `_forward_hooks` starts with an underscore: it is PyTorch's internal field.
  Here we look at it only to count; code does not write to it.
