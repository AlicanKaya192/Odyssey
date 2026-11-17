# Debugging

Bugs in deep learning come in two kinds. **Loud** bugs stop the program and
leave a message: a shape does not fit, a type does not fit. They are annoying
but easy, because the message points to the place. **Silent** bugs give no
message at all: the program runs, the loss is printed, only the model does
not learn, or learns worse than expected. In this section we see ways to
catch both, each with a check of a few lines.

## Following shapes layer by layer

The shortest way to find where a shape error comes from is to pass the input
through the layers one at a time and print the shape at each step. Walking
over an `nn.Sequential` is enough:

```python
import math

import torch
from torch import nn


def make_model():
    return nn.Sequential(nn.Flatten(), nn.Linear(64, 32), nn.ReLU(),
                         nn.Linear(32, 10))


torch.manual_seed(0)
model = make_model()
x = torch.randn(16, 8, 8)
h = x
for layer in model:
    h = layer(h)
    print(type(layer).__name__, tuple(h.shape))
```

```text
Flatten (16, 64)
Linear (16, 32)
ReLU (16, 32)
Linear (16, 10)
```

16 images of `(8, 8)` came in, `Flatten` opened each into 64 numbers, and the
two `Linear` layers brought them down to 32 and 10. If a layer receives a
shape it does not expect, this printout tells you **on which line** the error
happens.

## Three common messages

```python
loss_fn = nn.CrossEntropyLoss()
logits = model(x)
attempts = [
    lambda: loss_fn(logits, torch.zeros(16)),
    lambda: model(x.double()),
    lambda: loss_fn(logits, torch.zeros(16, 1, dtype=torch.long)),
]
for attempt in attempts:
    try:
        attempt()
    except RuntimeError as error:
        print(error)
```

```text
expected target dtype to be Long or Byte, but got Float
mat1 and mat2 must have the same dtype, but got Double and Float
0D or 1D target tensor expected, multi-target not supported
```

- **The target is a float:** `CrossEntropyLoss` wants class numbers, that is
  integers (`long`). Building the labels as floats like `torch.zeros(16)`
  gives this message. The fix: `y.long()`.
- **Mixed types:** an array coming from NumPy is often `float64` (`Double`),
  while the model's weights are `float32` (`Float`). The fix: `x.float()`.
- **The target has shape `(16, 1)`:** the target should be a flat list of
  class numbers, `(16,)`. The fix: `y.squeeze(1)` or `y.view(-1)`.

## Silent bug 1: the starting loss

Looking at the loss once before training starts tells a lot. A randomly
initialised model gives roughly equal probability to every class; with 10
classes that means 1/10 for each true class, and the loss is
`−log(1/10) = log 10 ≈ 2.3`:

```python
y = torch.randint(0, 10, (16,))
print(round(loss_fn(model(x), y).item(), 1), round(math.log(10), 1))

broken = make_model()
with torch.no_grad():
    for p in broken.parameters():
        p.mul_(20)
print(round(loss_fn(broken(x), y).item(), 1))
```

```text
2.3 2.3
92.6
```

- In the healthy model the starting loss is exactly where expected:
  2.3.
- The model whose weights were multiplied by 20 (wrongly initialised) has a
  loss of 92.6: before learning anything, it is very **sure** of
  its random answers. If the starting loss is far from `log(number of
  classes)`, look first at the initialisation, the scale of the input and the
  loss function.

## Silent bug 2: memorising a single batch

The fastest test of whether a model can learn at all: train **a single batch
of 8 examples** for hundreds of steps. A healthy model memorises this little
data and the loss drops to zero. If it does not, the problem is not in the
data but in the code, the training loop or the loss:

```python
def overfit_one_batch(bug):
    torch.manual_seed(0)
    net = make_model()
    if bug == "softmax":
        net.append(nn.Softmax(dim=1))
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    for step in range(200):
        optimizer.zero_grad()
        loss = loss_fn(net(x[:8]), y[:8])
        loss.backward()
        if bug != "no step":
            optimizer.step()
    return round(loss.item(), 2)


for bug in ["none", "softmax", "no step"]:
    print(bug, overfit_one_batch(bug))
```

```text
none 0.0
softmax 1.46
no step 2.26
```

- The bug-free model memorised the 8 examples: a loss of 0.
- The model with a softmax added at the end (`CrossEntropyLoss` wants logits;
  the Activations and Loss section) got stuck at 1.46: the loss
  goes down but cannot reach zero.
- The model whose `optimizer.step()` was forgotten never changed; the loss is
  the starting 2.26.
- This test told apart three situations that give no message at all. It is
  run before starting the real training and does not take even a minute.

## Silent bug 3: an accumulating gradient

`backward()` **adds** the gradient to `.grad`; it does not overwrite it. If
`zero_grad()` is forgotten, every step walks with the sum of all the previous
ones:

```python
w = torch.tensor(1.0, requires_grad=True)
for step in range(3):
    (3 * w).backward()
    print(w.grad.item())
```

```text
3.0
6.0
9.0
```

The gradient should have been 3 every time; it piled up as 3, 6, 9. Since the
step size grows from epoch to epoch, training becomes unstable. But an
optimizer like Adam, which divides the gradient by its own scale, can partly
hide this; that is why it is a silent bug, and when writing a loop
`zero_grad()` goes at the very start out of habit.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Shapes</span><span>Pass through the layers one by one and print the shape at each step.</span></div>
    <div class="anat-row"><span>Types</span><span>Input <code>float32</code>, class target <code>long</code> and flat <code>(n,)</code>.</span></div>
    <div class="anat-row"><span>Starting loss</span><span>In classification, is it around <code>log(number of classes)</code>?</span></div>
    <div class="anat-row"><span>One batch</span><span>Can it memorise 8 examples?</span></div>
    <div class="anat-row"><span>The loop</span><span>Are <code>zero_grad</code>, <code>backward</code>, <code>step</code> all there and in order?</span></div>
    <div class="anat-row"><span>Gradients</span><span>Is every parameter's <code>.grad</code> filled and finite?</span></div>
  </div>
  <figcaption>What to look at, in order, when a model does not learn.</figcaption>
</figure>

## Summary

- For a loud bug, read the message; find the place by printing the shape
  layer by layer.
- `CrossEntropyLoss`: target `long` and `(n,)`; input `float32`.
- The starting loss should be around `log(number of classes)`.
- The single-batch memorising test separates code bugs from data.
- If `zero_grad()` is forgotten, the gradient accumulates.
