import numpy as np
from ab_data import make_population

users = make_population()
x = users["minutes"].to_numpy()
rng = np.random.default_rng(11)
means = rng.choice(x, size=(3000, 4)).mean(axis=1)
print(4, round(means.mean(), 2))
# Do this in a loop for n = 4 and n = 64. On each line after n, write the
# mean of the means (2 places), the standard deviation of the means
# (3 places) and the formula x.std() / np.sqrt(n) (3 places).
