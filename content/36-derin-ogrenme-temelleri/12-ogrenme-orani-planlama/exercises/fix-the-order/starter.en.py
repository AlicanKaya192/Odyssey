import torch
from torch import nn
from torch.optim import lr_scheduler


def used_rates(epochs):
    w = nn.Parameter(torch.zeros(1))
    optimizer = torch.optim.SGD([w], lr=0.1)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)
    used = []
    for epoch in range(epochs):
        scheduler.step()
        used.append(optimizer.param_groups[0]["lr"])
        optimizer.step()
    return used

print(used_rates(6))
