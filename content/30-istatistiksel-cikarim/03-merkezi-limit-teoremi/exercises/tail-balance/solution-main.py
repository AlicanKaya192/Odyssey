import numpy as np
from ab_data import make_population

users = make_population()
y = users["spend"].to_numpy()
mu, sigma = y.mean(), y.std()
rng = np.random.default_rng(12)
for n in [30, 2000]:
    means = rng.choice(y, size=(2000, n)).mean(axis=1)
    se = sigma / np.sqrt(n)
    low = (means < mu - 1.96 * se).mean()
    high = (means > mu + 1.96 * se).mean()
    print(n, round(low, 3), round(high, 3))
