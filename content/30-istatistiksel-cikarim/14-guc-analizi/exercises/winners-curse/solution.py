import numpy as np
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(422)
n_group = 800
lifts, significant = [], []
for _ in range(1000):
    buy_a = rng.binomial(n_group, 0.10)
    buy_b = rng.binomial(n_group, 0.12)
    p = proportions_ztest([buy_b, buy_a], [n_group, n_group])[1]
    lifts.append((buy_b - buy_a) / n_group)
    significant.append(p < 0.05 and buy_b > buy_a)
lifts, significant = np.array(lifts), np.array(significant)
print(round(significant.mean(), 3))
print(round(lifts[significant].mean() / 0.02, 2))
