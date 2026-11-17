import torch
import torch.nn.functional as F


def nt_xent(z1, z2, tau):
    z = F.normalize(torch.cat([torch.tensor(z1), torch.tensor(z2)]), dim=1)
    sim = z @ z.T / tau
    sim.fill_diagonal_(float("-inf"))
    n = len(z1)
    target = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return round(F.cross_entropy(sim, target).item(), 3)

print(nt_xent([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], 0.5))
print(nt_xent([[1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0]], 0.5))
