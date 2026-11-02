import numpy as np
from ab_data import make_population

users = make_population()
y = users["spend"].to_numpy()
mu, sigma = y.mean(), y.std()
rng = np.random.default_rng(12)
# n = 30 ve n = 2000 için: 2000 örneklem ortalaması çek
# (rng.choice(y, size=(2000, n)).mean(axis=1)), se = sigma / np.sqrt(n)
# ve her satıra n, mu - 1.96 * se'nin altına düşenlerin payı ve
# mu + 1.96 * se'nin üstüne çıkanların payını (3 basamak) yaz.
