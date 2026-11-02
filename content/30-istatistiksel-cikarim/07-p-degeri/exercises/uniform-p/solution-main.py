import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["load_ms"].to_numpy()
rng = np.random.default_rng(101)
a = rng.choice(x, size=(4000, 60))
b = rng.choice(x, size=(4000, 60))
p = stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
print(round((p < 0.05).mean(), 3))
print(round((p < 0.10).mean(), 3))
print(np.histogram(p, bins=4, range=(0, 1))[0].tolist())
