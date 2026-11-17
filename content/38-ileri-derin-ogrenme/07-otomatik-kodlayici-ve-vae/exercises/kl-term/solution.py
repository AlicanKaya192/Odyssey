import torch


def kl_term(mu, logvar):
    mu, logvar = torch.tensor(mu), torch.tensor(logvar)
    kl = -0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))
    return round(kl.item(), 3) + 0.0

print(kl_term([[1.0, 1.0, 1.0, 1.0]], [[0.0, 0.0, 0.0, 0.0]]))
print(kl_term([[0.0, 0.0]], [[0.0, 0.0]]))
