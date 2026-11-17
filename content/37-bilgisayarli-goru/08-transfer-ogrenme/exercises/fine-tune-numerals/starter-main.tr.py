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


def transfer(state, x, y, x_test, y_test, fine_tune):
    torch.manual_seed(0)
    features = make_features()
    features.load_state_dict(state)
    model = nn.Sequential(features, nn.Linear(64, 10))
    return 0.0


from sklearn.datasets import load_digits

digits = load_digits()
x_all = F.interpolate(torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16,
                      size=16, mode="bilinear")
y_all = torch.tensor(digits.target)
order = torch.randperm(len(y_all), generator=torch.Generator().manual_seed(0))
train_idx = torch.cat([order[y_all[order] == d][:5] for d in range(10)])
test_mask = torch.ones(len(y_all), dtype=torch.bool)
test_mask[train_idx] = False
state = {k: v.clone() for k, v in source[0].state_dict().items()}

frozen_acc = transfer(state, x_all[train_idx], y_all[train_idx], x_all[test_mask], y_all[test_mask], False)
tuned_acc = transfer(state, x_all[train_idx], y_all[train_idx], x_all[test_mask], y_all[test_mask], True)
print(frozen_acc < 0.6, tuned_acc > 0.7)
print(tuned_acc > frozen_acc)
