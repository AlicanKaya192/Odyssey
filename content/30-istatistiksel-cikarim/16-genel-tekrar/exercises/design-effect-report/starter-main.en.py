import numpy as np
from scipy import stats
from ab_data import make_design_test

test = make_design_test(n=200, seed=612)
a = test.loc[test["group"] == "A", "minutes"].to_numpy()
b = test.loc[test["group"] == "B", "minutes"].to_numpy()
# Print, one per line:
# 1) the two medians (2 places)
# 2) Welch's t-test p, 3) Mann-Whitney's p (4 places)
# 4) Cohen's d (3 places); the groups are equal in size, the pooled
#    deviation is np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
