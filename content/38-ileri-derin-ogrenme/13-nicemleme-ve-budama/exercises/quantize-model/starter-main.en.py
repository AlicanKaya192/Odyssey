import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table

x, y = map(torch.tensor, make_table(1000, seed=7))
torch.manual_seed(0)
net = nn.Sequential(nn.Linear(6, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 3))
opt = torch.optim.Adam(net.parameters(), lr=0.01)
gen = torch.Generator().manual_seed(1)
for _ in range(30):
    perm = torch.randperm(800, generator=gen)
    for i in range(0, 800, 50):
        idx = perm[i:i + 50]
        opt.zero_grad()
        F.cross_entropy(net(x[idx]), y[idx]).backward()
        opt.step()
net.eval()


def accuracy(model):
    with torch.no_grad():
        return (model(x[800:]).argmax(1) == y[800:]).float().mean().item()


def quantize(w):
    scale = w.abs().max() / 127
    q = torch.round(w / scale).clamp(-127, 127).to(torch.int8)
    return q, scale


acc = accuracy(net)
stored = []
# For every Linear layer: quantise it, add the (q, scale) pair to stored,
# replace the weight with q.float() * scale (inside torch.no_grad)
print(len(stored), stored[0][0].dtype)
print(abs(accuracy(net) - acc) < 0.02)
