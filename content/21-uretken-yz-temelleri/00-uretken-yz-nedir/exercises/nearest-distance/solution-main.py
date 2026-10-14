import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def nearest_distances(points, name):
    part = X[y == name]
    scale = part.std(axis=0)
    a = np.asarray(points, dtype=float) / scale
    b = part / scale
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))
    return d.min(axis=1).round(3).tolist()


fish = [[33.5, 595.6], [29.0, 520.0], [45.0, 900.0]]
print(nearest_distances(fish, "bream"))
