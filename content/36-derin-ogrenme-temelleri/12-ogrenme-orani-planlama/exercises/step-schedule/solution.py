import torch
from torch import nn
from torch.optim import lr_scheduler


def step_rates(lr, step_size, gamma, epochs):
    w = nn.Parameter(torch.zeros(1))
    optimizer = torch.optim.SGD([w], lr=lr)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)
    rates = []
    for epoch in range(epochs):
        rates.append(round(optimizer.param_groups[0]["lr"], 6))
        optimizer.step()
        scheduler.step()
    return rates

print(step_rates(0.1, 2, 0.5, 5))
