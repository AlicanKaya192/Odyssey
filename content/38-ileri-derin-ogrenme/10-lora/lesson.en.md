# LoRA and Efficient Fine-Tuning

In the Generative AI Fundamentals module we explained LoRA (low-rank
adaptation) with NumPy. The idea: when adapting a trained model to a new
job, the **change** in the weights `ΔW` is often low-rank; we can write it as
the product of two thin matrices `B · A`. The original weight `W` is
**frozen**, only `A` and `B` are trained. The number of trained values drops
by orders of magnitude; the base model is not damaged, and the adaptation can
be plugged in and out as a separate small file.

<figure class="fig">
<div class="flow">
<span class="node">x</span><span class="arrow">→</span>
<span class="node">W (frozen)</span><span class="arrow">+</span>
<span class="node acc">B · A (trained)</span><span class="arrow">→</span>
<span class="node">output</span>
</div>
<figcaption>A LoRA layer: output = W·x + (α/r)·B·A·x. A narrows to rank r, B widens back.</figcaption>
</figure>

In this section we write the same idea in PyTorch as an `nn.Module`: choosing
which parameters are trained with `requires_grad`, counting the trained
parameters, and finally folding the adaptation into the weight.

## A LoRA layer

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table


class LoRALinear(nn.Module):
    def __init__(self, base, r=4, alpha=8):
        super().__init__()
        self.base = base.requires_grad_(False)
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale


torch.manual_seed(0)
layer = nn.Linear(64, 64)
lora = LoRALinear(layer, r=4)
x = torch.randn(5, 64)
print(torch.equal(lora(x), layer(x)))
trainable = sum(p.numel() for p in lora.parameters() if p.requires_grad)
print(trainable, layer.weight.numel() + layer.bias.numel())
```

```text
True
512 4160
```

- `base.requires_grad_(False)`: the base layer's weight and bias freeze; even
  if handed to an optimiser they do not change, and no derivative is
  computed.
- `B` starts at zero: at the start of training `B · A = 0`, so the LoRA layer
  gives **exactly the same** output as the base layer. The adaptation grows
  from zero.
- `A` starts with small random numbers; if both were zero the derivative
  would be zero too and neither would learn.
- In a 64 × 64 layer the base has 4160 values; a rank-4 LoRA trains
  `4 · 64 + 64 · 4 = 512` values.

## The base model and a new task

Let us train a classifier on the table data (6 features, 3 classes). In the
new task the data is of the same kind but **the order of the features has
changed**: as if a sensor's cables had been swapped. The base model does not
know this.

```python
xa, ya = map(torch.tensor, make_table(800, seed=7))
xb, yb = map(torch.tensor, make_table(800, seed=8))
xb = xb[:, [1, 0, 2, 5, 4, 3]]


def fit(model, x, y, epochs=30, lr=0.01):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=lr)
    gen = torch.Generator().manual_seed(1)
    for _ in range(epochs):
        perm = torch.randperm(600, generator=gen)
        for i in range(0, 600, 50):
            idx = perm[i:i + 50]
            opt.zero_grad()
            F.cross_entropy(model(x[idx]), y[idx]).backward()
            opt.step()


def accuracy(model, x, y):
    with torch.no_grad():
        return (model(x[600:]).argmax(1) == y[600:]).float().mean().item()


torch.manual_seed(0)
net = nn.Sequential(nn.Linear(6, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(),
                    nn.Linear(64, 3))
fit(net, xa, ya)
acc_a = accuracy(net, xa, ya)
print(round(acc_a, 1), round(accuracy(net, xb, yb), 1))
```

```text
0.8 0.5
```

- The first 600 rows are training, the last 200 test.
- The base model does well on its own task; on the new task it is wrong
  almost half the time.
- `fit` hands only the parameters with `requires_grad` to the optimiser;
  we will see why that matters below.

## Fine-tuning with LoRA

We freeze the whole network and wrap only the first layer in a rank-2 LoRA
layer.

```python
net.requires_grad_(False)
net[0] = LoRALinear(net[0], r=2)
fit(net, xb, yb)
trainable = sum(p.numel() for p in net.parameters() if p.requires_grad)
total = sum(p.numel() for p in net.parameters())
print(trainable, total)
print(accuracy(net, xb, yb) > 0.8)
plain = nn.Sequential(net[0].base, *net[1:])
print(accuracy(plain, xa, ya) == acc_a)
```

```text
140 4943
True
True
```

- Only 140 values are trained (`2 · 6 + 64 · 2`); the whole model has 4943.
  Less than three per cent.
- On the new task the accuracy rose above 0.8: the change in the order of the
  features can be met with a low-rank correction in the first layer.
- The last line: taking the adaptation out and using the base layer gives
  **exactly the same** accuracy on the old task. The base weights never
  changed.

## Folding the adaptation into the weight

When serving, computing two paths (`W·x` and `B·A·x`) on every call is
unnecessary. When training is over, `W' = W + (α/r) · B · A` is written as a
single weight; the output is the same and the speed is the base model's.

```python
def merge(lora):
    merged = nn.Linear(lora.base.in_features, lora.base.out_features)
    with torch.no_grad():
        merged.weight.copy_(lora.base.weight + lora.scale * lora.B @ lora.A)
        merged.bias.copy_(lora.base.bias)
    return merged


merged_net = nn.Sequential(merge(net[0]), *net[1:])
with torch.no_grad():
    print(torch.allclose(merged_net(xb), net(xb), atol=1e-5))
```

```text
True
```

Why `allclose`: the two paths do the same computation in a different order;
in floating-point addition the order can change the last digits.

## Summary

- LoRA: `W` frozen, `ΔW = B · A` trained; `B` starts at zero, so at the
  start the output is the base model's.
- In PyTorch freezing is `requires_grad_(False)`; give the optimiser only
  the parameters with `requires_grad`.
- The number of trained parameters is `r · (inputs + outputs)`.
- With the adaptation removed the base model is as it was.
- Before serving it can be folded into the weight with `W + (α/r)·B·A`.
