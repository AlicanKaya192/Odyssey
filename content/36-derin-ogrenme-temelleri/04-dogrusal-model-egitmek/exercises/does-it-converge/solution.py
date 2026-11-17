import numpy as np
import torch

rng = np.random.default_rng(2)
x = torch.tensor(rng.uniform(0, 3, 50), dtype=torch.float32)
y = 4 * x - 1


def converges(lr, steps=50):
    w = torch.zeros(1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    first = ((w * x + b - y) ** 2).mean().item()
    for _ in range(steps):
        loss = ((w * x + b - y) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()
    last = ((w * x + b - y) ** 2).mean().item()
    return last < first

for lr in [0.001, 0.05, 0.5]:
    print(lr, converges(lr))
