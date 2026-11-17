import numpy as np
import torch

rng = np.random.default_rng(6)
x_np = rng.uniform(0, 4, 80)
y_np = -2 * x_np + 1 + rng.normal(0, 0.3, 80)
x = torch.tensor(x_np, dtype=torch.float32)
y = torch.tensor(y_np, dtype=torch.float32)

w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
lr = 0.1
for step in range(500):
    # Compute the loss, backward, update inside no_grad, zero the gradients.
    pass

loss = ((w * x + b - y) ** 2).mean()
print("w =", round(w.item(), 1), "b =", round(b.item(), 1))
print(loss.item() < 0.2)
