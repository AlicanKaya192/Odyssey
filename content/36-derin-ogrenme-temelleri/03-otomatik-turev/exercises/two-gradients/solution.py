import torch


def gradients(w_value, x, b_value, target):
    w = torch.tensor(w_value, requires_grad=True)
    b = torch.tensor(b_value, requires_grad=True)
    loss = (w * x + b - target) ** 2
    loss.backward()
    return [w.grad.item(), b.grad.item()]

print(gradients(2.0, 3.0, 1.0, 5.0))
print(gradients(1.0, -1.0, 0.0, 0.0))
