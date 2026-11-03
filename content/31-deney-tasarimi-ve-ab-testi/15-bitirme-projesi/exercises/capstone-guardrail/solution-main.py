import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
buyers = test[test["bought"] == 1]
refunds = buyers.groupby("group")["refunded"].agg(["sum", "count"])
low_r, high_r = confint_proportions_2indep(
    refunds.loc["B", "sum"], refunds.loc["B", "count"],
    refunds.loc["A", "sum"], refunds.loc["A", "count"])
print(round(high_r * 100, 2))
print(high_r < 0.02)
