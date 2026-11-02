from statsmodels.stats.power import TTestIndPower
from ab_data import make_user_log

users = make_user_log(n=8000, seed=731)
d_min = TTestIndPower().solve_power(nobs1=10000, power=0.8, alpha=0.05)
# Print the minimum detectable relative effect with 10,000 per group for
# bought, minutes and revenue in order: the name and f"{x:.1%}".
# Relative MDE = d_min * deviation / mean.
