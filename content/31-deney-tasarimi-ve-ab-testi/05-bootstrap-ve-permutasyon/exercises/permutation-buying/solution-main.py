import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_experiment

test = make_experiment(n=6000, seed=753)
labels = (test["group"] == "B").to_numpy()
bought = test["bought"].to_numpy()
rng = np.random.default_rng(754)
observed = bought[labels].mean() - bought[~labels].mean()
count = 0
for _ in range(2000):
    shuffled = rng.permutation(labels)
    diff = bought[shuffled].mean() - bought[~shuffled].mean()
    count += abs(diff) >= abs(observed)
print(round(count / 2000, 3))
k_b, k_a = bought[labels].sum(), bought[~labels].sum()
p = proportions_ztest([k_b, k_a], [labels.sum(), (~labels).sum()])[1]
print(round(p, 3))
