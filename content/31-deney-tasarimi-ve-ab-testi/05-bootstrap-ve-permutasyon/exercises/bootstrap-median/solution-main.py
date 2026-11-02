import numpy as np
from ab_data import make_experiment

test = make_experiment(n=8000, seed=751)
buyers = test[test["bought"] == 1]
order_a = buyers.loc[buyers["group"] == "A", "revenue"].to_numpy()
order_b = buyers.loc[buyers["group"] == "B", "revenue"].to_numpy()
rng = np.random.default_rng(752)
diffs = []
for _ in range(1000):
    diffs.append(np.median(rng.choice(order_b, len(order_b)))
                 - np.median(rng.choice(order_a, len(order_a))))
print(round(np.median(order_a), 2), round(np.median(order_b), 2))
low, high = np.percentile(diffs, [2.5, 97.5])
print(round(low, 2), round(high, 2))
