import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def nearest_distances(points, name):
    return []


fish = [[33.5, 595.6], [29.0, 520.0], [45.0, 900.0]]
print(nearest_distances(fish, "bream"))
