import math
from statsmodels.stats.power import TTestIndPower


def split_sizes(d, share_b):
    n_a = TTestIndPower().solve_power(effect_size=d, power=0.8, alpha=0.05)
    n_a = math.ceil(n_a)
    return [n_a, n_a, 2 * n_a]


print(split_sizes(0.05, 0.5))
print(split_sizes(0.05, 0.2))
