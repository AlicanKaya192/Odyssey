# Quantisation and Pruning

There are two common ways to shrink a trained model. **Quantisation** writes
every weight with fewer bits: an 8-bit integer instead of a 32-bit
`float32`. **Pruning** zeroes unimportant weights or removes them altogether.
Both shrink the model and speed it up on suitable hardware; the price may be
a little accuracy. In this section we measure both: how much smaller it got,
how much accuracy was lost.

## The starting model

```python
import warnings
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table

x, y = map(torch.tensor, make_table(1000, seed=7))


def train():
    torch.manual_seed(0)
    net = nn.Sequential(nn.Linear(6, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(),
                        nn.Linear(64, 3))
    opt = torch.optim.Adam(net.parameters(), lr=0.01)
    gen = torch.Generator().manual_seed(1)
    for _ in range(30):
        perm = torch.randperm(800, generator=gen)
        for i in range(0, 800, 50):
            idx = perm[i:i + 50]
            opt.zero_grad()
            F.cross_entropy(net(x[idx]), y[idx]).backward()
            opt.step()
    return net.eval()


def accuracy(model):
    with torch.no_grad():
        return (model(x[800:]).argmax(1) == y[800:]).float().mean().item()


net = train()
acc = accuracy(net)
print(acc > 0.8, sum(p.numel() for p in net.parameters()))
```

```text
True 4803
```

`train()` builds the same model with the same seed on every call; below we
try every method on its own copy of the same model.

## Quantising by hand: scale and rounding

The simplest form is **symmetric, per-tensor** quantisation: a **scale** is
chosen so that the largest absolute value in the tensor maps to 127; every
weight is divided by the scale, rounded and stored as `int8`. When used, it is
multiplied by the scale to restore it.

```python
def quantize(w):
    scale = w.abs().max() / 127
    q = torch.round(w / scale).clamp(-127, 127).to(torch.int8)
    return q, scale


w = net[2].weight.detach()
q, scale = quantize(w)
restored = q.float() * scale
print(q.dtype, q.shape, w.element_size() // q.element_size())
print(bool((w - restored).abs().max() <= scale / 2 + 1e-6))
```

```text
torch.int8 torch.Size([64, 64]) 4
True
```

- Same shape, type `int8`: 1 byte per number instead of 4, **4 times**
  smaller. The scale is a single number per tensor; its cost is negligible.
- The rounding error is at most half a scale: every weight was rounded to the
  nearest "step".

## How much accuracy was lost?

Let us quantise and restore the weights of all linear layers and measure on
the same test data:

```python
qnet = train()
with torch.no_grad():
    for m in qnet:
        if isinstance(m, nn.Linear):
            q, scale = quantize(m.weight)
            m.weight.copy_(q.float() * scale)
print(abs(accuracy(qnet) - acc) < 0.02)
```

```text
True
```

With 8 bits the accuracy barely changed (on this computer the difference is
under one per cent). Bringing the weights down to 256 steps hardly affects
this model's decisions. In large models 8 bits are usually safe too; at 4
bits and below careful methods are needed.

## PyTorch's dynamic quantisation

PyTorch has a ready way to do the same: **dynamic quantisation** converts the
weights to `int8` in advance and quantises the activations while running.
For linear layers it is the easiest method.

```python
warnings.simplefilter("ignore")
from torch.ao.quantization import quantize_dynamic

dnet = quantize_dynamic(train(), {nn.Linear}, dtype=torch.qint8)
kind = type(dnet[0])
print(kind.__name__, "quantized" in kind.__module__, dnet[0].weight().dtype)
print(dnet(x[:5]).dtype, abs(accuracy(dnet) - acc) < 0.05)
```

```text
Linear True torch.qint8
torch.float32 True
```

- The linear layers were replaced with their quantised versions: the name is
  still `Linear`, but it comes from `torch.ao.nn.quantized`; the weight type
  is `qint8`. Input and output are still `float32`: from the outside the model
  looks the same.
- `warnings.simplefilter("ignore")` on purpose: in this version
  `torch.ao.quantization` warns that it is "deprecated". PyTorch is moving
  quantisation into a separate package (`torchao`), which is not installed in
  this program. The idea and the result are the same.
- The quantised layers compute on a processor-specific back end (`onednn` on
  this computer, another back end on Macs). So the detailed result may vary
  a little between machines; we printed only that the accuracy stayed close.

## Pruning

`torch.nn.utils.prune.l1_unstructured` zeroes the weights of a layer that are
smallest in absolute value. Let us prune first half, then nine tenths:

```python
import torch.nn.utils.prune as prune

half = train()
prune.l1_unstructured(half[2], "weight", amount=0.5)
print(int((half[2].weight == 0).sum()), half[2].weight.numel())
print(abs(accuracy(half) - acc) < 0.05)
most = train()
prune.l1_unstructured(most[2], "weight", amount=0.9)
print(accuracy(most) < acc - 0.05)
```

```text
2048 4096
True
True
```

- 2048 of the middle layer's 4096 weights are zero; the accuracy stayed close.
- With nine tenths pruned the accuracy dropped clearly. How much can be pruned
  is found by measuring; often a short retraining (fine-tuning) after pruning
  brings part of the loss back.

Pruning has a trap: the zeros still take up space. The weight matrix has the
same size, it is only sparse inside. To really shrink it you need either
sparse matrix formats and hardware that uses them, or **structured pruning**,
which removes a whole neuron (row); we do the latter in the notes.

## Summary

- Quantisation: scale = largest |w| / 127, `round(w / scale)` → `int8`; 4
  times smaller, at 8 bits the accuracy is almost the same.
- `quantize_dynamic`: linear layers become `qint8`, input and output stay
  `float32`; the result may vary a little with the back end.
- Pruning: zeroes small weights; how much to prune is chosen by measuring.
- Sparse pruning does not shrink the size by itself; structured pruning does.
