import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def n_for_rates(p_a, p_b):
    effect = proportion_effectsize(p_b, p_a)
    n = NormalIndPower().solve_power(effect_size=effect, power=0.8, alpha=0.05)
    return int(np.ceil(n))


print(n_for_rates(0.10, 0.12))
print(n_for_rates(0.20, 0.25))
