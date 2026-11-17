# Weight Initialisation and Normalisation

As a network gets deeper, a new problem appears: the signal can grow or die
out as it passes through the layers. Each layer multiplies its input by a
matrix; if the factors are a little large, the numbers explode in ten
layers, and if they are a little small, they sink to zero. The gradients
walk the same road backwards in backpropagation and share the same fate. In
this section we see two remedies: **initialising the weights at the right
scale** and putting a **normalisation** layer between the layers.

## The signal in ten layers

Let us pass a random input through ten `Linear + ReLU` layers whose weights
are initialised in different ways and look at the standard deviation of the
output. The numbers can be huge or tiny, so we print their base-10 logarithm
(`3` → a thousand, `−3` → a thousandth):

```python
import math

import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(512, 256)


def depth_test(init):
    torch.manual_seed(1)
    h = x
    for _ in range(10):
        layer = nn.Linear(256, 256, bias=False)
        init(layer.weight)
        h = torch.relu(layer(h))
    return h.std().item()


for name, init in [("std 1.0", lambda w: nn.init.normal_(w, std=1.0)),
                   ("std 0.01", lambda w: nn.init.normal_(w, std=0.01)),
                   ("kaiming", lambda w: nn.init.kaiming_normal_(w, nonlinearity="relu")),
                   ("default", lambda w: None)]:
    print(name, round(math.log10(depth_test(init)), 1))
```

```text
std 1.0 10.4
std 0.01 -9.6
kaiming -0.1
default -3.9
```

- With weights of standard deviation 1, the output is around 10¹⁰: it
  exploded. With 0.01 it is around 10⁻¹⁰: it died out. In both cases the
  gradients either overflow or vanish; the network cannot learn.
- **Kaiming (He) initialisation** picks the standard deviation from the
  number of inputs: `sqrt(2 / inputs)`. ReLU zeros half the signal, and the
  factor 2 makes up for it; after ten layers the signal is still around 1
  (log ≈ 0).
- PyTorch's default initialisation for `nn.Linear` is fine for one layer but
  slowly shrinks the signal in a deep ReLU stack (10⁻⁴). In deep networks with
  ReLU, setting the initialisation to Kaiming explicitly is a good habit.

<figure class="fig">
  <div class="versus">
    <div class="no"><h5>Too large / too small</h5>The signal grows or dies layer by layer; the gradients overflow or vanish.</div>
    <div class="ok"><h5>Kaiming / Xavier</h5>The scale is picked from the number of inputs; the signal keeps its size through the depth.</div>
  </div>
  <figcaption>Kaiming (<code>kaiming_normal_</code>) for networks with ReLU, Xavier (<code>xavier_normal_</code>) for networks with tanh/sigmoid.</figcaption>
</figure>

## BatchNorm

Initialisation only fixes the **start**; as training goes on, the layers'
inputs can drift again. **Batch normalisation** (BatchNorm) normalises each
feature by subtracting the mean of the examples in the batch and dividing by
their standard deviation; then it applies a learned scale and shift.

```python
bn = nn.BatchNorm1d(3)
batch = torch.tensor([[1.0, 100.0, -5.0], [3.0, 300.0, -5.5],
                      [5.0, 200.0, -4.5], [7.0, 400.0, -5.0]])
out = bn(batch)
print([round(v, 3) + 0.0 for v in out.mean(dim=0).tolist()])
print([round(v, 3) for v in out.std(dim=0, unbiased=False).tolist()])
print([round(v, 1) for v in bn.running_mean.tolist()])
```

```text
[0.0, 0.0, 0.0]
[1.0, 1.0, 1.0]
[0.4, 25.0, -0.5]
```

- The three columns were on completely different scales (ones, hundreds,
  minus fives); each column now has mean 0 and standard deviation 1. (The
  `+ 0.0` prints tiny negative numbers that round to `-0.0` as a plain `0.0`.)
- `running_mean` is a moving average of the means seen during training; it
  started at 0 and moved a tenth (momentum 0.1) of the way to this batch's
  means. In evaluation (`eval()`) these stored values are used instead of
  the batch's: when predicting, even a single example may come, and the
  result must not depend on the other examples in the batch.

## The effect of BatchNorm

Let us train a deep eight-layer network that uses sigmoid with the same
settings, once without BatchNorm and once with BatchNorm after every layer:

```python
from dl_data import make_table

x_np, y_np = make_table(1000)
X, Y = torch.from_numpy(x_np), torch.from_numpy(y_np)


def deep_net(batch_norm):
    torch.manual_seed(0)
    layers, n_in = [], 6
    for _ in range(8):
        layers.append(nn.Linear(n_in, 32))
        if batch_norm:
            layers.append(nn.BatchNorm1d(32))
        layers.append(nn.Sigmoid())
        n_in = 32
    return nn.Sequential(*layers, nn.Linear(32, 3))


for batch_norm in [False, True]:
    model = deep_net(batch_norm)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        loss = loss_fn(model(X[:800]), Y[:800])
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        accuracy = (model(X[800:]).argmax(dim=1) == Y[800:]).float().mean().item()
    print(batch_norm, round(loss.item(), 2), round(100 * accuracy, 1))
```

```text
False 1.1 33.5
True 0.35 88.5
```

- The network without BatchNorm learned nothing: the loss got stuck at
  `log 3 ≈ 1.10` and the test accuracy is 33.5% (as good as
  always naming one class in three-class data). The gradient passing
  through eight sigmoids sinks almost to zero (the **vanishing gradient**).
- The same network with BatchNorm learned with the same learning rate: a
  test accuracy of 88.5%.

## LayerNorm

BatchNorm looks at the examples in the batch; it struggles when the batch is
very small or the examples are sequences of different lengths (text).
**LayerNorm** normalises each example within itself, over its features; it
does not depend on the batch:

```python
ln = nn.LayerNorm(3)
out = ln(batch)
print([round(v, 2) for v in out[0].tolist()])
print([round(v, 3) + 0.0 for v in out.mean(dim=1).tolist()])
```

```text
[-0.64, 1.41, -0.77]
[0.0, 0.0, 0.0, 0.0]
```

The mean of each **row** became 0. Transformers (the advanced module) use
LayerNorm everywhere; image networks commonly use BatchNorm.

## Summary

- With the wrong weight scale the signal explodes or dies out with depth.
- `nn.init.kaiming_normal_` for deep networks with ReLU.
- BatchNorm normalises each feature over the batch; it uses the batch in
  training and the stored averages in evaluation. It makes deep networks
  easier to train.
- LayerNorm normalises each example within itself; it does not depend on the
  batch.
