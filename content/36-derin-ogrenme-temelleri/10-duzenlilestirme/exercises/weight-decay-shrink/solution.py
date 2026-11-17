import torch


def after_decay(start, lr, decay, steps):
    w = torch.tensor([start], requires_grad=True)
    optimizer = torch.optim.SGD([w], lr=lr, weight_decay=decay)
    for _ in range(steps):
        optimizer.zero_grad()
        (w * 0).sum().backward()
        optimizer.step()
    return round(w.item(), 4)

print(after_decay(1.0, 0.1, 0.1, 3))
print(after_decay(2.0, 0.5, 0.2, 2))
