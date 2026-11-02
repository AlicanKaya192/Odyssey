import math
from statsmodels.stats.power import TTestIndPower


def n_for_lift(mean, sd, lift):
    n = TTestIndPower().solve_power(effect_size=lift, power=0.8, alpha=0.05)
    return math.ceil(n)


print(n_for_lift(0.117, 0.32, 0.05))
print(n_for_lift(21.1, 23.3, 0.02))
