import numpy as np
from statsmodels.stats.power import TTestIndPower


def n_per_group(d):
    n = TTestIndPower().solve_power(effect_size=d, power=0.5, alpha=0.05)
    return int(np.ceil(n))


print(n_per_group(0.5))
print(n_per_group(0.2))
