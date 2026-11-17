import torch


def reparameterize(mu, logvar, eps):
    mu, logvar, eps = torch.tensor(mu), torch.tensor(logvar), torch.tensor(eps)
    z = mu + torch.exp(0.5 * logvar) * eps
    return [round(v, 3) for v in z.tolist()]

print(reparameterize([0.0, 1.0], [0.0, 0.0], [1.0, -1.0]))
print(reparameterize([2.0], [-1.3862944], [1.0]))
