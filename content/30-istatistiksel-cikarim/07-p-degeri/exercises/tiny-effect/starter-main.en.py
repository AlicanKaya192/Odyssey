import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(103)
a = rng.choice(x, size=50000)
b = rng.choice(x, size=50000) * 1.02
# 1) Print p from stats.ttest_ind(b, a, equal_var=False) in scientific
#    notation: f"{p:.1e}"
# 2) Print the difference of the means in SECONDS (minutes * 60) with
#    1 place.
