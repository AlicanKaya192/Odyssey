import numpy as np
from ab_data import make_population

users = make_population()
y = users["spend"].to_numpy()
mu, sigma = y.mean(), y.std()
rng = np.random.default_rng(12)
# For n = 30 and n = 2000: draw 2000 sample means
# (rng.choice(y, size=(2000, n)).mean(axis=1)), se = sigma / np.sqrt(n)
# and on each line write n, the share below mu - 1.96 * se and the share
# above mu + 1.96 * se (3 places).
