import torch


def descend(start, lr, steps):
    w = torch.tensor(start, requires_grad=True)
    optimizer = torch.optim.SGD([w], lr=lr)
    for _ in range(steps):
        optimizer.zero_grad()
        loss = (w - 3) ** 2
        loss.backward()
        optimizer.step()
    return round(w.item(), 4)

print(descend(0.0, 0.1, 10))
print(descend(10.0, 0.5, 1))
