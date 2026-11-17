Sparse pruning leaves the zeros inside the matrix. **Structured pruning**
zeroes a whole row, that is, a neuron; that neuron is no longer connected to
any input and can really be removed from the layer. The model shrinks and
gets faster on ordinary hardware too.

```python
import torch
import torch.nn.utils.prune as prune
from torch import nn

torch.manual_seed(0)
fc1, fc2 = nn.Linear(6, 64), nn.Linear(64, 3)
model = nn.Sequential(fc1, nn.ReLU(), fc2).eval()
prune.ln_structured(fc1, "weight", amount=0.5, n=2, dim=0)
prune.remove(fc1, "weight")
keep = fc1.weight.abs().sum(dim=1) > 0
print(int(keep.sum()), tuple(fc1.weight.shape))
```

```text
32 (64, 6)
```

- `ln_structured(..., n=2, dim=0)`: looks at the L2 norm of the rows (dim 0)
  and zeroes the smallest half. 32 of 64 neurons are left.
- `prune.remove` makes the pruning permanent (writes the pruning mask into the
  weight). The shape is still `(64, 6)`: to save space the layer has to be
  rebuilt.

The pruned neuron's weights are zero but its **bias** is not: that neuron
gives every input the same constant value (`ReLU(bias)`). If, when removing
it, we fold that constant into the next layer's bias, the output is kept
exactly:

```python
n = int(keep.sum())
small1, small2 = nn.Linear(6, n), nn.Linear(n, 3)
with torch.no_grad():
    small1.weight.copy_(fc1.weight[keep])
    small1.bias.copy_(fc1.bias[keep])
    small2.weight.copy_(fc2.weight[:, keep])
    small2.bias.copy_(fc2.bias + fc2.weight[:, ~keep] @ torch.relu(fc1.bias[~keep]))
small = nn.Sequential(small1, nn.ReLU(), small2).eval()


def count(m):
    return sum(p.numel() for p in m.parameters())


x = torch.randn(10, 6)
with torch.no_grad():
    print(torch.allclose(small(x), model(x), atol=1e-6))
print(count(model), count(small))
```

```text
True
643 323
```

- The small model gives the same output as the pruned model; the parameter
  count dropped to about half.
- `fc2.weight[:, ~keep] @ relu(fc1.bias[~keep])`: the constant contribution of
  the removed neurons; it was added to the next layer's bias.

In real networks this is done on convolution channels (filter pruning), and a
short fine-tuning is usually added after each pruning step. The order is
always the same: prune, measure accuracy, retrain if needed, really shrink
the layer.
