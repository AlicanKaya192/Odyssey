import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["load_ms"].to_numpy()
rng = np.random.default_rng(101)
a = rng.choice(x, size=(4000, 60))
b = rng.choice(x, size=(4000, 60))
# 1) A two-sample t-test for every pair of rows:
#    stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
# 2) The share with p < 0.05 and with p < 0.10 (3 places)
# 3) np.histogram(p, bins=4, range=(0, 1))[0].tolist()
