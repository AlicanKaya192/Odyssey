import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
for n in [30, 120, 480]:
    x = users.sample(n=n, random_state=52)["minutes"]
    se = x.std() / np.sqrt(n)
    low, high = stats.t.interval(0.95, df=n - 1, loc=x.mean(), scale=se)
    print(n, round(float(high - low), 2))
