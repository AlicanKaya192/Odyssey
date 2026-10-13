import numpy as np


def unit(direction):
    d = np.array(direction, dtype=float)
    return d / np.linalg.norm(d)


def projection(v, direction):
    return round(float(np.array(v) @ unit(direction)), 3)


def neutralize(v, direction):
    g = unit(direction)
    v = np.array(v, dtype=float)
    return (v - (v @ g) * g).round(3).tolist()

v = [3.0, 4.0]
print(projection(v, [1.0, 0.0]))
print(neutralize(v, [1.0, 0.0]))
print(neutralize(v, [1.0, 1.0]))
