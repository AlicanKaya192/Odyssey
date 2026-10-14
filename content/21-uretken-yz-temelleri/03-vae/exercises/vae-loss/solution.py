import numpy as np

x = [[0.0, 1.0, 1.0], [1.0, 0.0, 0.0]]
out = [[0.1, 0.8, 0.7], [0.9, 0.2, 0.4]]
mu = [[0.5, -1.0], [0.0, 2.0]]
logvar = [[0.0, -1.0], [0.5, 0.0]]


def vae_loss(x, out, mu, logvar, beta):
    x, out = np.array(x), np.array(out)
    mu, logvar = np.array(mu), np.array(logvar)
    rec = -(x * np.log(out) + (1 - x) * np.log(1 - out)).sum(axis=1).mean()
    kl = (0.5 * (mu ** 2 + np.exp(logvar) - logvar - 1).sum(axis=1)).mean()
    return [round(float(rec), 4), round(float(kl), 4), round(float(rec + beta * kl), 4)]


print(vae_loss(x, out, mu, logvar, 1.0))
print(vae_loss(x, out, mu, logvar, 0.5))
