import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sequences


class Detector(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(10, 8)
        self.conv = nn.Conv1d(8, 16, kernel_size=2)
        self.head = nn.Linear(16, 2)

    def forward(self, ids):
        h = self.embed(ids).transpose(1, 2)
        return self.head(torch.relu(self.conv(h)).amax(dim=2))


x_np, y_np = make_sequences(600, seed=7)
x, y = torch.tensor(x_np), torch.tensor(y_np)
torch.manual_seed(0)
model = Detector()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
gen = torch.Generator().manual_seed(1)
for epoch in range(20):
    perm = torch.randperm(500, generator=gen)
    for i in range(0, 500, 50):
        idx = perm[i:i + 50]
        opt.zero_grad()
        F.cross_entropy(model(x[idx]), y[idx]).backward()
        opt.step()
model.eval()
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x[:4],), dynamic_shapes=({0: batch},))
torch.export.save(ep, "detector.pt2")

with torch.no_grad():
    acc = (model(x[500:]).argmax(1) == y[500:]).float().mean().item()
    golden = model(x[500:])
loaded = torch.export.load("detector.pt2").module()
print(acc > 0.95)
print(torch.allclose(loaded(x[500:]), golden, atol=1e-5), loaded(x[:3]).shape)
