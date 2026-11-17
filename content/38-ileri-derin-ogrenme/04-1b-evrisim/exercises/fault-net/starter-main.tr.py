import torch
from torch import nn
from dl_data import make_sensor

xs, ys = make_sensor(300, length=64, seed=11)
x = torch.from_numpy(xs).unsqueeze(1)
y = torch.from_numpy(ys)


class FaultNet(nn.Module):
    def __init__(self):
        super().__init__()
        # self.features: iki Conv1d + ReLU ve AdaptiveMaxPool1d(1)
        self.features = nn.Sequential()
        self.head = nn.Linear(8, 2)

    def forward(self, x):
        return self.head(self.features(x).squeeze(-1))


torch.manual_seed(0)
model = FaultNet()
print(tuple(model.features(x[:2]).shape))
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x[:200], y[:200]), batch_size=32, shuffle=True,
    generator=torch.Generator().manual_seed(0))
opt = torch.optim.Adam(model.parameters(), lr=0.01)
for epoch in range(15):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        nn.functional.cross_entropy(model(xb), yb).backward()
        opt.step()
model.eval()
with torch.no_grad():
    acc = (model(x[200:]).argmax(dim=1) == y[200:]).float().mean().item()
print(acc > 0.9)
