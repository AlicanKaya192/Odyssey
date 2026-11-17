# Optimisation Algorithms

Gradient descent moved a parameter a small step against its gradient:
`w ← w − lr · gradient`. This rule has a weakness: it uses the same
learning rate in every direction. When the loss is steep in one direction
and flat in another (which is always the case in neural networks), it
either bounces in the steep direction or crawls in the flat one. In this
section we compare PyTorch's optimizers (`SGD`, `SGD` with momentum, `Adam`)
through this weakness.

## A long valley

Consider a loss with two parameters: `10·w₁² + w₂²`. The best point is
`(0, 0)`. The valley is ten times steeper in the `w₁` direction. Let us
write a small function that runs an optimizer for 50 steps and returns the
remaining loss:

```python
import torch


def bowl(w):
    return 10 * w[0] ** 2 + w[1] ** 2


def run(make_optimizer, steps=50):
    w = torch.tensor([1.0, 1.0], dtype=torch.float64, requires_grad=True)
    optimizer = make_optimizer([w])
    for _ in range(steps):
        optimizer.zero_grad()
        bowl(w).backward()
        optimizer.step()
    return bowl(w).item()


for lr in [0.01, 0.09, 0.11]:
    loss = run(lambda p: torch.optim.SGD(p, lr=lr))
    print("SGD", lr, round(loss, 3) if loss < 1000 else "> 1000")
```

```text
SGD 0.01 0.133
SGD 0.09 0.0
SGD 0.11 > 1000
```

- `lr = 0.01`: the steep direction (`w₁`) is done quickly, but the flat
  direction (`w₂`) is still on its way after 50 steps; the loss is
  0.133.
- `lr = 0.09`: good; but in the steep direction every step crosses to the
  other side of the valley (a zigzag).
- `lr = 0.11`: the steep direction diverges and the loss explodes. For SGD
  the **steepest direction** sets the upper limit of the learning rate;
  that is also why the flat direction is slow.

## Momentum

**Momentum** does not use the gradient directly; it builds up a
**velocity**: at each step the velocity is most of the previous velocity
plus the new gradient. Gradients pointing the same way add up and
accelerate; zigzagging gradients cancel each other out.

```python
for momentum in [0.0, 0.9]:
    loss = run(lambda p: torch.optim.SGD(p, lr=0.01, momentum=momentum))
    print("momentum", momentum, round(loss, 3))
```

```text
momentum 0.0 0.133
momentum 0.9 0.015
```

With the same small learning rate, momentum moved much faster in the flat
direction: the loss is about 9 times smaller. `momentum=0.9`
is the most common value.

## Adam

**Adam** combines two ideas: like momentum it keeps an average of the
gradient, and it also keeps, for each parameter, an average of the
gradient's size and divides the step by it. So each parameter moves **on its
own scale**: the step shrinks in the steep direction and grows in the flat
one.

```python
for lr in [0.01, 0.1]:
    print("Adam", lr, round(run(lambda p: torch.optim.Adam(p, lr=lr)), 3))
```

```text
Adam 0.01 3.17
Adam 0.1 0.0
```

- With `lr = 0.1`, Adam finished the flat direction quickly too.
- With `lr = 0.01` it is slow: in Adam one step is roughly the size of the
  learning rate, whatever the gradient. In 50 steps it can travel at most
  about 0.5. Read Adam's learning rate as "the step size per parameter".

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>SGD(lr)</code></span><span>Step = lr · gradient. Simple, needs no memory; the steepest direction limits the learning rate.</span></div>
    <div class="anat-row"><span><code>SGD(lr, momentum=0.9)</code></span><span>Builds up a velocity from the gradients; damps the zigzag, speeds up along flat directions.</span></div>
    <div class="anat-row"><span><code>Adam(lr)</code></span><span>Sets each parameter's step by its own gradient size. A good start for most problems; typical lr 0.001–0.01.</span></div>
  </div>
  <figcaption>The three optimizers in brief.</figcaption>
</figure>

## On a real network

Let us make the same comparison with the digit network from the
introduction: two optimizers, 40 epochs, the same starting weights.

```python
from torch import nn
from sklearn.datasets import load_digits

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)


def train(make_optimizer, epochs=40):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
    optimizer = make_optimizer(model.parameters())
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(X[:1200]), y[:1200])
        loss.backward()
        optimizer.step()
    return loss.item()


print("SGD ", round(train(lambda p: torch.optim.SGD(p, lr=0.1)), 2))
print("Adam", round(train(lambda p: torch.optim.Adam(p, lr=0.01)), 2))
```

```text
SGD  2.11
Adam 0.16
```

After 40 epochs SGD's loss is still high and Adam's is much lower. This does
not mean Adam is always better: well-tuned SGD with momentum ends up as good
as Adam on many image models, sometimes better. But Adam starts fast with
little tuning; we will mostly use it in this module.

## Summary

- SGD uses the same learning rate in every direction; the steepest direction
  sets the limit and flat directions stay slow.
- Momentum builds a velocity from the gradients and damps the zigzag.
- Adam sets each parameter's step on its own scale; lr ≈ the step size.
- Whatever the optimizer, the training loop is the same: `zero_grad`,
  `backward`, `step`.
