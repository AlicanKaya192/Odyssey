import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(103)
a = rng.choice(x, size=50000)
b = rng.choice(x, size=50000) * 1.02
# 1) stats.ttest_ind(b, a, equal_var=False) ile p'yi bilimsel gösterimle
#    yazdır: f"{p:.1e}"
# 2) Ortalamalar farkını SANİYE olarak (dakika * 60) 1 basamakla yazdır.
