import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
# Compute the 95% interval of the refund rate difference among buyers
# (B first).
# 1) Print the top end in points with 2 places.
# 2) Is the top end below 2 points (0.02)? Print True / False.
