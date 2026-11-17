import torch
from torch import nn


def same_twice():
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Dropout(0.5), nn.Linear(32, 2))
    x = torch.ones(1, 4)
    with torch.no_grad():
        train_same = torch.equal(model(x), model(x))
        model.eval()
        eval_same = torch.equal(model(x), model(x))
    return [train_same, eval_same]

print(same_twice())
