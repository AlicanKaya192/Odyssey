import torch
from torch import nn

torch.manual_seed(0)
real = -2 + 0.5 * torch.randn(2000, 1, generator=torch.Generator().manual_seed(1))
G = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
D = nn.Sequential(nn.Linear(1, 16), nn.LeakyReLU(0.2), nn.Linear(16, 1))
loss_fn = nn.BCEWithLogitsLoss()
opt_g = torch.optim.Adam(G.parameters(), lr=0.002, betas=(0.5, 0.999))
opt_d = torch.optim.Adam(D.parameters(), lr=0.002, betas=(0.5, 0.999))
gen = torch.Generator().manual_seed(2)
ones, zeros = torch.ones(64, 1), torch.zeros(64, 1)

for step in range(800):
    xb = real[torch.randint(0, len(real), (64,), generator=gen)]
    fake = G(torch.randn(64, 4, generator=gen))
    # 1) Train the discriminator: 1 for real, 0 for fake.detach()
    # 2) Train the generator: ask for 1 for D(fake)

with torch.no_grad():
    s = G(torch.randn(2000, 4, generator=torch.Generator().manual_seed(3)))
    p = torch.sigmoid(D(s)).mean().item()
print(abs(s.mean().item() + 2) < 0.3)
print(abs(p - 0.5) < 0.05)
