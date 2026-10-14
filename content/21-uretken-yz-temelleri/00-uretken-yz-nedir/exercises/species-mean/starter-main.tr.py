import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def species_mean(name):
    # X[y == name] o türün balıkları
    return []


print(species_mean("perch"))
print(species_mean("bream"))
