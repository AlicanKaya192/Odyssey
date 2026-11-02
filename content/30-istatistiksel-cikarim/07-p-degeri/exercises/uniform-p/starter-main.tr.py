import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["load_ms"].to_numpy()
rng = np.random.default_rng(101)
a = rng.choice(x, size=(4000, 60))
b = rng.choice(x, size=(4000, 60))
# 1) Her satır çifti için iki örneklem t-testi:
#    stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
# 2) p < 0.05 ve p < 0.10 olanların payı (3 basamak)
# 3) np.histogram(p, bins=4, range=(0, 1))[0].tolist()
