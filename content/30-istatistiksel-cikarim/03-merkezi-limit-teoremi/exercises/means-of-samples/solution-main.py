import numpy as np
from ab_data import make_population

users = make_population()
x = users["minutes"].to_numpy()
rng = np.random.default_rng(11)
for n in [4, 64]:
    means = rng.choice(x, size=(3000, n)).mean(axis=1)
    print(n, round(means.mean(), 2), round(means.std(), 3),
          round(x.std() / np.sqrt(n), 3))
