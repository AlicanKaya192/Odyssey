import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def sample_fish(name, n, seed):
    return []


for fish in sample_fish("bream", 3, 1):
    print(fish)
