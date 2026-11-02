import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_experiment

test = make_experiment(n=6000, seed=753)
labels = (test["group"] == "B").to_numpy()
bought = test["bought"].to_numpy()
rng = np.random.default_rng(754)
observed = bought[labels].mean() - bought[~labels].mean()
# 1) 2000 times shuffle the labels (rng.permutation(labels)), compute the
#    difference; count it if its absolute value is at least the real one.
# 2) Print the permutation p, then the two-proportion z-test p, 3 places.
