import torch
from torch import nn

x = torch.linspace(-1, 1, 50).unsqueeze(1)
y = 2 * x + 1


def fit_save_load():
    torch.manual_seed(0)
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()
    for step in range(300):
        optimizer.zero_grad()
        loss_fn(model(x), y).backward()
        optimizer.step()
    torch.manual_seed(1)
    fresh = nn.Linear(1, 1)
    same = torch.equal(model(x), fresh(x))
    return [round(fresh.weight.item(), 1), round(fresh.bias.item(), 1), same]

print(fit_save_load())
