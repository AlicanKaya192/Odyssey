import numpy as np

x = [[0.0, 1.0, 1.0], [1.0, 0.0, 0.0]]
out = [[0.1, 0.8, 0.7], [0.9, 0.2, 0.4]]
mu = [[0.5, -1.0], [0.0, 2.0]]
logvar = [[0.0, -1.0], [0.5, 0.0]]


def vae_loss(x, out, mu, logvar, beta):
    return [0.0, 0.0, 0.0]


print(vae_loss(x, out, mu, logvar, 1.0))
print(vae_loss(x, out, mu, logvar, 0.5))
