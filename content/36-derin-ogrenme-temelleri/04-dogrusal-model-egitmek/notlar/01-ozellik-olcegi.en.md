The learning rate is not chosen on its own; it depends on the scale of the
input. Imagine we measured the same points in millimetres instead of
centimetres (`x · 100`):

```python
import math


def fit(inputs, lr, steps=100):
    w = torch.zeros(1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    for _ in range(steps):
        loss = ((w * inputs + b - y) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()
    return loss.item()


big = x * 100
print(math.isfinite(fit(big, 0.05)), round(fit(big, 0.00001), 2))
scaled = (big - big.mean()) / big.std()
print(round(fit(scaled, 0.05), 3))
```

```text
False 1.23
0.235
```

- When the input grows 100 times, the gradient of `w` grows too; the
  lesson's suitable `lr = 0.05` now diverges: the result is not even a
  finite number (`math.isfinite` is `False`); the loss overflowed to `nan`.
- A smaller learning rate stops the explosion, but now `b` learns very
  slowly; after 100 rounds the loss is still high (1.23).
- **Scaling** the input (mean 0, standard deviation 1) solves both: with the
  same `lr = 0.05` the loss comes down to the noise level again.

That is why inputs are almost always scaled in deep learning: pulling pixel
values into 0–1, standardising table columns. The `/ 16` in the
introduction is for this too.
