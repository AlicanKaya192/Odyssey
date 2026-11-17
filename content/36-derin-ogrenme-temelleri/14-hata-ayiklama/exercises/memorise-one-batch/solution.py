import torch
from torch import nn

x = torch.randn(8, 5, generator=torch.Generator().manual_seed(1))
y = torch.arange(8) % 4


def overfit_one_batch():
    torch.manual_seed(0)
    net = nn.Sequential(nn.Linear(5, 16), nn.ReLU(), nn.Linear(16, 4))
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    loss_fn = nn.CrossEntropyLoss()
    for step in range(300):
        optimizer.zero_grad()
        loss = loss_fn(net(x), y)
        loss.backward()
        optimizer.step()
    return loss.item() < 0.05

print(overfit_one_batch())
