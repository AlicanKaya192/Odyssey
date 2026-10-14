import numpy as np


def kl_term(mu, logvar):
    return 0.0


print(kl_term([0.0, 0.0], [0.0, 0.0]))
print(kl_term([2.0, 0.0], [0.0, 0.0]))
print(kl_term([0.0, 0.0], [-2.0, 0.0]))
