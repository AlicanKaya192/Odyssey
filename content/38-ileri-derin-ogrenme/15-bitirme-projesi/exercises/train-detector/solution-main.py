import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x = torch.tensor(x_np * gain).unsqueeze(1)
y = torch.tensor(y_np)
torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv1d(1, 16, 5, padding=2), nn.ReLU(), nn.MaxPool1d(2),
    nn.Conv1d(16, 32, 5, padding=2), nn.ReLU(), nn.AdaptiveMaxPool1d(1),
    nn.Flatten(), nn.Linear(32, 2))
opt = torch.optim.Adam(model.parameters(), lr=0.003)
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x[:400], y[:400]), batch_size=32, shuffle=True,
    generator=torch.Generator().manual_seed(1))
for epoch in range(10):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        opt.step()
model.eval()
with torch.no_grad():
    pred = model(x[500:]).argmax(dim=1)
acc = (pred == y[500:]).float().mean().item()
recall = ((pred == 1) & (y[500:] == 1)).sum().item() / (y[500:] == 1).sum().item()

print(acc > 0.9, recall > 0.8)
