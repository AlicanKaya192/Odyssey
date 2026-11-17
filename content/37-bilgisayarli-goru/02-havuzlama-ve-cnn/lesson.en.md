# Pooling and the CNN Architecture

A convolution layer extracts feature maps from a picture. A classifier needs
two more things: **shrinking** the maps (so there is less computation and the
next layers look at a wider area) and, at the end, going from maps to
**class scores**. In this section we build the pooling layer and the skeleton
of a **convolutional neural network** (CNN) that brings these together. We
will not train it yet; we will learn to follow the shape of the data after
each layer.

## Max pooling

**Pooling** splits a map into small squares and leaves one number per square.
**Max pooling** takes the largest value of the square, **average pooling** its
mean. A 2 × 2 pooling halves the map's size.

```python
import torch
import torch.nn.functional as F

fmap = torch.tensor([
    [1, 3, 2, 0],
    [4, 6, 1, 1],
    [0, 2, 9, 5],
    [1, 1, 3, 7],
], dtype=torch.float32).reshape(1, 1, 4, 4)
print(F.max_pool2d(fmap, 2)[0, 0].tolist())
print(F.avg_pool2d(fmap, 2)[0, 0].tolist())
```

```text
[[6.0, 2.0], [2.0, 9.0]]
[[3.5, 1.0], [1.0, 6.0]]
```

- The top-left square is `1, 3, 4, 6`: its largest is 6, its mean 3.5.
- Pooling has no weights to learn; it is just a rule.

## Robustness to small shifts

Max pooling answers "is the pattern somewhere in this square?"; to some extent
it forgets **exactly where**. This makes small shifts harmless:

```python
a = torch.zeros(1, 1, 4, 4)
b = torch.zeros(1, 1, 4, 4)
c = torch.zeros(1, 1, 4, 4)
a[0, 0, 0, 0] = 1
b[0, 0, 1, 1] = 1
c[0, 0, 2, 2] = 1
print(torch.equal(F.max_pool2d(a, 2), F.max_pool2d(b, 2)))
print(torch.equal(F.max_pool2d(a, 2), F.max_pool2d(c, 2)))
```

```text
True
False
```

- In `a` and `b` the dot moved inside the same 2 × 2 square: the pooled map is
  the same.
- In `c` the dot moved into another square: the map changed. Pooling adds
  **some**, not **complete**, robustness to shifts. As layers stack up, this
  robustness grows.

## The skeleton of a CNN

A typical classifier CNN consists of a pattern repeated a few times:
**convolution → ReLU → pooling**. With each repeat the map shrinks and the
number of channels grows: as the picture gets smaller, more and more complex
patterns are kept at each position. At the end the map is flattened
(`Flatten`) and a fully connected layer gives the class scores. ReLU is the
activation function that turns negative values into zero; you know it from
the Deep Learning Fundamentals module.

```python
from torch import nn

model = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(16 * 4 * 4, 3),
)
x = torch.zeros(1, 1, 16, 16)
for layer in model:
    x = layer(x)
    print(f"{type(layer).__name__:<10} {tuple(x.shape)}")
```

```text
Conv2d     (1, 8, 16, 16)
ReLU       (1, 8, 16, 16)
MaxPool2d  (1, 8, 8, 8)
Conv2d     (1, 16, 8, 8)
ReLU       (1, 16, 8, 8)
MaxPool2d  (1, 16, 4, 4)
Flatten    (1, 256)
Linear     (1, 3)
```

- The convolutions keep the size with `padding=1`; each `MaxPool2d(2)` halves
  it: 16 → 8 → 4.
- `Flatten` turns the `(16, 4, 4)` map into a list of 256 numbers. The 256 in
  `Linear(16 * 4 * 4, 3)` comes exactly from here; if it is written wrong the
  network raises a shape error on its first run.
- The output is one score per class: `(1, 3)`.

## Where are the parameters?

```python
for name, p in model.named_parameters():
    print(f"{name:<9} {tuple(p.shape)}")
print(sum(p.numel() for p in model.parameters()))

mlp = nn.Sequential(nn.Flatten(), nn.Linear(256, 64), nn.ReLU(), nn.Linear(64, 3))
print(sum(p.numel() for p in mlp.parameters()))
```

```text
0.weight  (8, 1, 3, 3)
0.bias    (8,)
3.weight  (16, 8, 3, 3)
3.bias    (16,)
7.weight  (3, 256)
7.bias    (3,)
2019
16643
```

- `0.weight`: `nn.Sequential` names layers by their position; `0` is the first
  convolution, `7` the last `Linear`.
- The CNN's total is about eight times smaller than a small fully connected
  network (MLP) with one hidden layer (2,019 against 16,643). And the CNN's
  parameters sit in kernels that look for patterns at every position.

## The receptive field

A single number in a layer is influenced by how large a part of the input
picture? This area is called the **receptive field**. In the first 3 × 3
convolution it is 3 × 3 pixels; every layer after a pooling sees a wider
area. The calculation is simple: each layer grows the receptive field by
`(kernel − 1) × jump`, where the "jump" is the product of the strides so far.

```python
layers = [("conv", 3, 1), ("pool", 2, 2), ("conv", 3, 1), ("pool", 2, 2)]
field, jump = 1, 1
for name, k, s in layers:
    field += (k - 1) * jump
    jump *= s
    print(name, field)
```

```text
conv 3
pool 4
conv 8
pool 10
```

After the second convolution each number sees an 8 × 8 part of the 16 × 16
picture. In deep networks the last layers see almost the whole picture; the
first layers catch small patterns such as edges, the last ones large patterns
such as shapes.

## Any size of picture: global average pooling

The network above only works with 16 × 16 pictures: the `Linear` layer
expects exactly 256 numbers. Modern networks use **global average pooling**
before flattening: each channel's whole map comes down to a single number,
its mean. `nn.AdaptiveAvgPool2d(1)` does this, and the output's size becomes
independent of the input's size.

```python
flexible = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Linear(16, 3),
)
for size in (16, 24, 32):
    print(size, tuple(flexible(torch.zeros(2, 1, size, size)).shape))
```

```text
16 (2, 3)
24 (2, 3)
32 (2, 3)
```

The last `Linear` now needs only 16 numbers (one mean per channel). The same
network accepts pictures of three different sizes. Famous architectures such
as ResNet end the same way; we will see them later.

## Summary

- Pooling shrinks the map; max pooling adds some robustness to small shifts
  and has no learned weights.
- The CNN pattern: (convolution → ReLU → pooling) × a few, then `Flatten` and
  `Linear`. The map shrinks, the channels grow.
- Following the shape through the layers: `for layer in model: x = layer(x)`.
- The receptive field grows layer by layer; `AdaptiveAvgPool2d(1)` makes the
  network independent of the input size.
