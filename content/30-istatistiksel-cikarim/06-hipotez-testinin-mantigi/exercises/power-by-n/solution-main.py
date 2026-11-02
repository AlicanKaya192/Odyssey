import numpy as np
from scipy import stats
from ab_data import make_population

old = make_population()["load_ms"].to_numpy()
rng = np.random.default_rng(83)
for n in [20, 80]:
    slower = rng.choice(old, size=(3000, n)) + 40
    p = stats.ttest_1samp(slower, old.mean(), axis=1).pvalue
    print(n, round((p < 0.05).mean(), 3))
