import torch
from torch import nn
from torch.optim import lr_scheduler


def warmup_rates(base, warm, epochs):
    w = nn.Parameter(torch.zeros(1))
    optimizer = torch.optim.SGD([w], lr=base)

    def factor(epoch):
        return min(1.0, (epoch + 1) / warm)

    scheduler = lr_scheduler.LambdaLR(optimizer, factor)
    rates = []
    for epoch in range(epochs):
        rates.append(round(optimizer.param_groups[0]["lr"], 4))
        optimizer.step()
        scheduler.step()
    return rates

print(warmup_rates(0.1, 4, 6))
