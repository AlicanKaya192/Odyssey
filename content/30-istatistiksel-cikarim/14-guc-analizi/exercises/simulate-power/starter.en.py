import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(421)
n_group = 2000
hits = 0
for _ in range(1000):
    buy_a = rng.binomial(n_group, 0.10)
    buy_b = rng.binomial(n_group, 0.12)
    hits += buy_b > buy_a
print(hits / 1000)
h = proportion_effectsize(0.12, 0.10)
power = NormalIndPower().power(effect_size=h, nobs1=n_group, alpha=0.05)
print(round(power, 3))
