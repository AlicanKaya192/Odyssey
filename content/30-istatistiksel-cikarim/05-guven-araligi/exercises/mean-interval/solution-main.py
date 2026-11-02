import numpy as np
from scipy import stats
from ab_data import make_population

users = make_population()
x = users.sample(n=60, random_state=51)["load_ms"]
mean = x.mean()
se = x.std() / np.sqrt(len(x))
low, high = stats.t.interval(0.95, df=len(x) - 1, loc=mean, scale=se)
print(round(mean, 1))
print(round(float(low), 1), round(float(high), 1))
