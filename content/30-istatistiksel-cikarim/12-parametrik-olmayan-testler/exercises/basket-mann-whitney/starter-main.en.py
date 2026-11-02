import numpy as np
from scipy import stats
from ab_data import make_basket_test

test = make_basket_test(n=150, seed=211)
a = test.loc[test["group"] == "A", "basket"].to_numpy()
b = test.loc[test["group"] == "B", "basket"].to_numpy()
print(round(np.median(a), 1), round(np.median(b), 1))
# 1) Print p from stats.mannwhitneyu(b, a) with 4 places.
# 2) Print the common language effect size U / (n_A * n_B) with 3 places.
