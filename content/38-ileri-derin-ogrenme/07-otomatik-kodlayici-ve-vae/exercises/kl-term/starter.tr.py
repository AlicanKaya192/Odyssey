import torch


def kl_term(mu, logvar):
    # Kodunu buraya yaz
    return 0.0

print(kl_term([[1.0, 1.0, 1.0, 1.0]], [[0.0, 0.0, 0.0, 0.0]]))
print(kl_term([[0.0, 0.0]], [[0.0, 0.0]]))
