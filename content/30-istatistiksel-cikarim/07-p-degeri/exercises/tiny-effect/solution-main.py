import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(103)
a = rng.choice(x, size=50000)
b = rng.choice(x, size=50000) * 1.02
result = stats.ttest_ind(b, a, equal_var=False)
seconds = (b.mean() - a.mean()) * 60
print(f"{result.pvalue:.1e}")
print(round(seconds, 1))
