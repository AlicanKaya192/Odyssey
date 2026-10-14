import numpy as np


def kl_term(mu, logvar):
    mu = np.array(mu)
    logvar = np.array(logvar)
    kl = 0.5 * (mu ** 2 + np.exp(logvar) - logvar - 1).sum()
    return round(float(kl), 4)


print(kl_term([0.0, 0.0], [0.0, 0.0]))
print(kl_term([2.0, 0.0], [0.0, 0.0]))
print(kl_term([0.0, 0.0], [-2.0, 0.0]))
