import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def species_mean(name):
    part = X[y == name]
    return part.mean(axis=0).round(1).tolist()


print(species_mean("perch"))
print(species_mean("bream"))
