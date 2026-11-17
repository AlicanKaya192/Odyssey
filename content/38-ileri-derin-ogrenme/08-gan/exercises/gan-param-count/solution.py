from torch import nn


def gan_param_count(z_dim, hidden):
    G = nn.Sequential(nn.Linear(z_dim, hidden), nn.ReLU(), nn.Linear(hidden, 1))
    D = nn.Sequential(nn.Linear(1, hidden), nn.LeakyReLU(0.2), nn.Linear(hidden, 1))
    return [sum(p.numel() for p in m.parameters()) for m in (G, D)]

print(gan_param_count(4, 16))
print(gan_param_count(2, 8))
