import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
# In this scenario B has no effect (lift=0.0).
# 1) Print the SRM p (stats.chisquare) with 3 places.
# 2) Print the 95% interval of the buying difference (B first) in points
#    with 2 places.
