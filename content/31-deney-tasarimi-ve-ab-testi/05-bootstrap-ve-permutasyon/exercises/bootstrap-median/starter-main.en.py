import numpy as np
from ab_data import make_experiment

test = make_experiment(n=8000, seed=751)
buyers = test[test["bought"] == 1]
order_a = buyers.loc[buyers["group"] == "A", "revenue"].to_numpy()
order_b = buyers.loc[buyers["group"] == "B", "revenue"].to_numpy()
rng = np.random.default_rng(752)
# 1) 1000 times: resample B, then A, with replacement and append the
#    median difference (B - A) to a list.
# 2) Print the two groups' medians, then the difference's 95% interval,
#    with 2 places.
