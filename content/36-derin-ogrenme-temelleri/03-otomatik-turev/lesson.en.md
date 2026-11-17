# Automatic Differentiation

To train a model we need the **gradient** of every parameter: if that
parameter grows a little, by how much and in which direction does the loss
change? In the Neural Networks section of the ML Algorithms module we
derived these derivatives by hand with the chain rule; every new layer meant
a new formula. PyTorch's **automatic differentiation** (autograd) system
does this for us: it records every operation we do with tensors and, when we
say `backward()`, computes the derivatives from the end back to the start.

## The first derivative

If we say `requires_grad=True` for a tensor, PyTorch starts tracking the
operations done with it:

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x
y.backward()
print(y.item(), x.grad.item())
```

```text
10.0 7.0
```

- `y = x² + 3x` is `4 + 6 = 10` at `x = 2`.
- Its derivative is `2x + 3`; `7` at `x = 2`. `backward()` computed this
  number and wrote it into `x.grad`. We did not write the formula.

## The computation graph

PyTorch adds every operation to a **computation graph**. The `grad_fn` of
each result says which operation produced it:

```python
a = torch.tensor(1.0, requires_grad=True)
b = 3 * a + 1
c = b ** 2
print(type(b.grad_fn).__name__, type(c.grad_fn).__name__)
print(a.grad_fn, a.is_leaf, c.is_leaf)
c.backward()
print(a.grad.item())
```

```text
AddBackward0 PowBackward0
None True False
24.0
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">a = 1</span><span class="arrow">→</span>
    <span class="node">b = 3a + 1<br><small>AddBackward0</small></span><span class="arrow">→</span>
    <span class="node">c = b²<br><small>PowBackward0</small></span>
  </div>
  <figcaption>The forward pass goes left to right; <code>backward()</code> walks the graph right to left and applies the chain rule.</figcaption>
</figure>

- We built `a` ourselves: it is a **leaf** of the graph and has no
  `grad_fn`. Parameters are always leaves; their gradients collect in their
  `.grad`.
- The chain rule: `dc/da = dc/db · db/da = 2b · 3`. At `a = 1`, `b = 4`
  and the result is `2 · 4 · 3 = 24`.

## Several inputs, vectors

A loss usually depends on many parameters. A single `backward()` computes
all their gradients at once:

```python
w = torch.tensor([1.0, -2.0, 0.5], requires_grad=True)
x = torch.tensor([3.0, 1.0, 2.0])
b = torch.tensor(0.0, requires_grad=True)
loss = ((w * x).sum() + b - 4) ** 2
loss.backward()
print(loss.item(), w.grad.tolist(), b.grad.item())
```

```text
4.0 [-12.0, -4.0, -8.0] -4.0
```

- The prediction is `w · x + b = 3 - 2 + 1 + 0 = 2`, the target 4, the loss
  `(2 - 4)² = 4`.
- `d loss / d w = 2 · (2 - 4) · x = -4x` → `[-12, -4, -8]`;
  `d loss / d b = -4`.
- We did not say `requires_grad` for `x`; the data is fixed and needs no
  gradient.
- A gradient has the same shape as its parameter: `w` is three numbers, so
  `w.grad` is three numbers too.

## Gradients accumulate

`backward()` **adds** the gradient to `.grad`; it does not overwrite it:

```python
x = torch.tensor(2.0, requires_grad=True)
for step in range(3):
    y = x ** 2
    y.backward()
    print(step, x.grad.item())
x.grad.zero_()
print(x.grad.item())
```

```text
0 4.0
1 8.0
2 12.0
0.0
```

The derivative is 4 every time, but `x.grad` grows 4, 8, 12. The
`optimizer.zero_grad()` at the start of the training loop prevents exactly
this: each round's gradient should come only from that round's loss.
Accumulation is sometimes used on purpose (adding up the gradients of small
batches when memory is short), but usually it is a forgotten `zero_grad`.

## `backward` starts from one number

`backward()` can only be called on a **single-number** (scalar) result:

```python
w = torch.tensor([1.0, 2.0], requires_grad=True)
out = w * 3
try:
    out.backward()
except RuntimeError as error:
    print(error)
out.sum().backward()
print(w.grad.tolist())
```

```text
grad can be implicitly created only for scalar outputs
[3.0, 3.0]
```

Loss functions already average over all the examples and give one number.
When you take the derivative of a computation of your own, finish it with
`.sum()` or `.mean()`.

## Comparing with a hand derivative

We can test that automatic differentiation is right with a **numerical
derivative**: `(f(x + h) − f(x − h)) / 2h`. In ML Algorithms we checked our
hand-written backward pass the same way.

```python
def f(t):
    return t ** 3 - 2 * t


x = torch.tensor(1.5, dtype=torch.float64, requires_grad=True)
f(x).backward()
h = 1e-4
numeric = (f(1.5 + h) - f(1.5 - h)) / (2 * h)
print(x.grad.item(), round(numeric, 4))
```

```text
4.75 4.75
```

`3x² − 2` is `6.75 − 2 = 4.75` at `x = 1.5`. Both agree. The difference: a
numerical derivative runs the function twice for every parameter, which is
impossible with millions of parameters. Automatic differentiation gives them
all in one backward pass.

## Summary

- Operations with tensors that have `requires_grad=True` are recorded in a
  computation graph; `backward()` computes the gradients with the chain rule.
- A gradient sits in the parameter's `.grad`, in the same shape as the
  parameter.
- `backward()` adds gradients; every training round needs `zero_grad`.
- `backward()` starts from a single number; the loss already is one.
