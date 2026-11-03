import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
# Apply CUPED to revenue (covariate pre_spend).
# 1) Print the correlation of pre_spend with revenue with 2 places.
# 2) Print the remaining variance ratio (adjusted / raw) with 3 places.
