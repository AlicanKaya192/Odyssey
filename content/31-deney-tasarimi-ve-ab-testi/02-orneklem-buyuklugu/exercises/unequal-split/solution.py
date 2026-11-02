import math
from statsmodels.stats.power import TTestIndPower


def split_sizes(d, share_b):
    ratio = share_b / (1 - share_b)
    n_a = TTestIndPower().solve_power(effect_size=d, power=0.8, alpha=0.05,
                                      ratio=ratio)
    n_a = math.ceil(n_a)
    n_b = math.ceil(n_a * ratio)
    return [n_a, n_b, n_a + n_b]


print(split_sizes(0.05, 0.5))
print(split_sizes(0.05, 0.2))
