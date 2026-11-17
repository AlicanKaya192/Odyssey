# A Linear Model with Gradient Descent

We now have two tools: tensors and automatic differentiation. In this
section we use them to train our first model **from scratch**: a line,
`y = w·x + b`. Without ready-made layers or an optimizer, we write every step
of gradient descent ourselves. Then we do the same job with PyTorch's
ready-made pieces and see that the two are the same. This is the job
`LinearRegression` did in the machine learning track; the difference is
that here we find the solution by **searching** for it step by step.

## The data

Let us make 100 points whose true relationship is `y = 3x + 2`, with noise
added on top. Because we know the true values, we can see whether the model
finds them.

```python
import numpy as np
import torch

rng = np.random.default_rng(0)
x_np = rng.uniform(0, 5, 100)
y_np = 3 * x_np + 2 + rng.normal(0, 0.5, 100)
x = torch.tensor(x_np, dtype=torch.float32)
y = torch.tensor(y_np, dtype=torch.float32)
print(x.shape, y.shape, x.dtype)
```

```text
torch.Size([100]) torch.Size([100]) torch.float32
```

We built the data with NumPy's seeded generator; the same 100 points come
out on every computer.

## The model and the loss

The model is just two numbers: the slope `w` and the constant `b`. We start
both at zero and ask for gradients. The loss is the **mean squared error**
(MSE): the mean of the squared differences between prediction and truth.

```python
w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)


def predict(x):
    return w * x + b


def mse(pred, target):
    return ((pred - target) ** 2).mean()


loss = mse(predict(x), y)
loss.backward()
print(round(loss.item()), round(w.grad.item()), round(b.grad.item()))
```

```text
124 -70 -20
```

- The model says 0 for every point; the loss is large (124).
- Both gradients are **negative**: if `w` or `b` grows, the loss falls. So
  gradient descent moves the parameter **against** the gradient:
  `w ← w − lr · w.grad`.

## The training loop

Now we repeat this step. Each round: predict, compute the loss, `backward`,
update both parameters, zero the gradients.

```python
w.grad.zero_()
b.grad.zero_()
lr = 0.05
for step in range(301):
    loss = mse(predict(x), y)
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    w.grad.zero_()
    b.grad.zero_()
    if step % 100 == 0:
        print(step, round(loss.item(), 3))
print("w =", round(w.item(), 1), "b =", round(b.item(), 1))
```

```text
0 124.456
100 0.238
200 0.235
300 0.235
w = 3.0 b = 2.0
```

- The loss drops quickly and settles around 0.235. It does not
  reach zero because the data is noisy: no line can pass through all 100
  points. The noise has a standard deviation of 0.5, a square of 0.25: the
  remaining loss is around that.
- The model found the true values: `w ≈ 3`, `b ≈ 2`. We built no formula;
  we only took small steps in the direction that lowers the loss.

## The learning rate

The value of `lr` changes everything. Let us run the same loop for 100
rounds with three learning rates:

```python
def train(lr, steps=100):
    w = torch.zeros(1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    for _ in range(steps):
        loss = ((w * x + b - y) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()
    return loss.item()


print(round(train(0.001), 2))
print(round(train(0.05), 2))
print(train(0.1) > 1e6)
```

```text
2.26
0.24
True
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h5>Too small (0.001)</h5>The right direction but very slow: after 100 rounds the loss is still large.</div>
    <div class="ok"><h5>Suitable (0.05)</h5>The loss comes down to the noise level.</div>
    <div class="no"><h5>Too large (0.1)</h5>Every step jumps too far to the other side of the valley; the loss explodes.</div>
  </div>
  <figcaption>The learning rate is the step size: too small is slow, too large is unstable.</figcaption>
</figure>

With a learning rate that is too large, each update throws the parameter to
the other side of the best value, farther than before. The difference
between 0.05 and 0.1 is only a factor of two, but one comes down and the
other explodes; the loss grows every round (divergence). A loss that comes
out as `nan` or huge usually means the learning rate is too high.

## The same job with ready-made pieces

PyTorch has a ready-made version of every piece of this loop: `nn.Linear(1,
1)` for the model, `nn.MSELoss()` for the loss and `torch.optim.SGD` for the
update.

```python
from torch import nn

model = nn.Linear(1, 1)
nn.init.zeros_(model.weight)
nn.init.zeros_(model.bias)
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
loss_fn = nn.MSELoss()
X = x.unsqueeze(1)
Y = y.unsqueeze(1)
for step in range(301):
    optimizer.zero_grad()
    loss = loss_fn(model(X), Y)
    loss.backward()
    optimizer.step()
print(X.shape, round(loss.item(), 3))
print("w =", round(model.weight.item(), 1), "b =", round(model.bias.item(), 1))
```

```text
torch.Size([100, 1]) 0.235
w = 3.0 b = 2.0
```

- `nn.Linear` wants its input as `(count, features)`; we turned the
  single-feature `x` into `(100, 1)` with `unsqueeze(1)`.
- We started the weights from zero (`nn.init.zeros_`), as in the
  hand-written version; the result is the same.
- The four steps we wrote by hand are here too: `zero_grad`, the loss,
  `backward`, `step`. `optimizer.step()` applies the same thing as our
  `w -= lr * w.grad` line to every parameter. The digit model in the
  introduction did exactly this; only its model was bigger.

## Summary

- Gradient descent: compute the loss, take the gradient, move the parameter
  against the gradient by `lr`, zero the gradient; repeat.
- The parameter update is done inside `torch.no_grad()`.
- A small learning rate is slow, a large one diverges.
- `nn.Linear`, `nn.MSELoss` and `optim.SGD` are the ready-made form of the
  same algorithm.
