import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from dl_data import make_shapes


def make_features():
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(),
    )


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


x_src, y_src = map(torch.from_numpy, make_shapes(600, seed=1))
torch.manual_seed(0)
source = nn.Sequential(make_features(), nn.Linear(64, 3))
optimizer = torch.optim.Adam(source.parameters(), lr=0.005)
loader = DataLoader(TensorDataset(x_src, y_src), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
for epoch in range(5):
    source.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        F.cross_entropy(source(xb), yb).backward()
        optimizer.step()


def train_head(model, x, y):
    for p in model[0].parameters():
        p.requires_grad = False
    optimizer = torch.optim.Adam(model[1].parameters(), lr=0.005)
    loader = DataLoader(TensorDataset(x, y), batch_size=8, shuffle=True,
                        generator=torch.Generator().manual_seed(0))
    for epoch in range(20):
        model.train()
        model[0].eval()
        for xb, yb in loader:
            optimizer.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            optimizer.step()


x_a, y_a = map(torch.from_numpy, make_shapes(24, seed=5))
x_at, y_at = map(torch.from_numpy, make_shapes(300, seed=6))
y_a, y_at = (y_a != 0).long(), (y_at != 0).long()
torch.manual_seed(0)
model = nn.Sequential(source[0], nn.Linear(64, 2))
weight_before = model[0][0].weight.clone()
stats_before = model[0][1].running_mean.clone()
train_head(model, x_a, y_a)
print(torch.equal(model[0][0].weight, weight_before))
print(torch.equal(model[0][1].running_mean, stats_before))
print(accuracy(model, x_at, y_at) > 0.9)
