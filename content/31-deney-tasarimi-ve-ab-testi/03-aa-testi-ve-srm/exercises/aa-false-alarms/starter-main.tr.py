import numpy as np
from scipy import stats
from ab_data import make_user_log

users = make_user_log(n=4000, seed=741)
rng = np.random.default_rng(742)
bought = users["bought"]
p_values = []
for _ in range(400):
    in_b = rng.random(len(users)) < 0.5
    test = stats.ttest_ind(bought[in_b], bought[~in_b], equal_var=False)
    p_values.append(test.pvalue)
p_values = np.array(p_values)
print(round(float((p_values < 0.5).mean()), 3))
