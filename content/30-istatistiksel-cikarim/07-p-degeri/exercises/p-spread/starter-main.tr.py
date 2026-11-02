import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(102)
a = rng.choice(x, size=(2000, 300))
b = rng.choice(x, size=(2000, 300)) * 1.10
p = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue
print(round(p[0], 3))
# Tek deneyin p'si yanıltır. Bunun yerine: p < 0.05 olanların payını
# (3 basamak) ve p'nin 10., 50., 90. yüzdeliklerini yaz:
# np.round(np.percentile(p, [10, 50, 90]), 3).tolist()
