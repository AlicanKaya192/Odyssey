import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def histogram_sample(name, bins, n, seed):
    weights = X[y == name, 1]
    counts, edges = np.histogram(weights, bins=bins)
    p = counts / counts.sum()
    g = np.random.default_rng(seed)
    box = g.choice(len(p), size=n, p=p)
    fake = g.uniform(edges[box], edges[box + 1])
    return [round(float(fake.mean()), 1), round(float(fake.std()), 1)]


print(histogram_sample("bream", 10, 5000, 5))
print(histogram_sample("perch", 4, 2000, 1))
