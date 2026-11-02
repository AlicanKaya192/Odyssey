import numpy as np
from ab_data import make_population

users = make_population()
true_mean = users["minutes"].mean()
means = []
for seed in range(500):
    sample = users["minutes"].sample(n=50, random_state=seed)
    means.append(sample.mean())
means = np.array(means)
print(round(means.min(), 2))
print(round(means.max(), 2))
close = np.abs(means - true_mean) <= 1
print(round(close.mean(), 3))
