import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(102)
a = rng.choice(x, size=(2000, 300))
b = rng.choice(x, size=(2000, 300)) * 1.10
p = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue
print(round(p[0], 3))
# One experiment's p misleads. Instead print the share with p < 0.05
# (3 places) and the 10th, 50th and 90th percentiles of p:
# np.round(np.percentile(p, [10, 50, 90]), 3).tolist()
