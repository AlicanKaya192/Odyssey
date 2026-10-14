import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def histogram_sample(name, bins, n, seed):
    weights = X[y == name, 1]
    return [0.0, 0.0]


print(histogram_sample("bream", 10, 5000, 5))
print(histogram_sample("perch", 4, 2000, 1))
