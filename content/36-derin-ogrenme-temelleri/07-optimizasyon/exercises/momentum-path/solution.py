import torch


def path(momentum):
    w = torch.tensor(0.0, requires_grad=True)
    optimizer = torch.optim.SGD([w], lr=0.1, momentum=momentum)
    positions = []
    for _ in range(4):
        optimizer.zero_grad()
        ((w - 3) ** 2).backward()
        optimizer.step()
        positions.append(round(w.item(), 4))
    return positions

print(path(0.0))
print(path(0.9))
