import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=84, lift=0.06)
# In this project B's true effect is 6% (relative).
# 1) Print the SRM p with 3 places.
# 2) Print the 95% interval of the buying difference (B first) in points
#    with 2 places.
# 3) Print the variance left after CUPED for revenue (1 - rho ** 2; rho is
#    the correlation of pre_spend with revenue) with 3 places.
