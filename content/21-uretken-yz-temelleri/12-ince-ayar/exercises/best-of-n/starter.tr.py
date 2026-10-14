import numpy as np


def best_of_n(candidates, weights):
    return []


cands = [[[1, 0, 1.0], [0, 1, 0.5]], [[0, 0, 2.0], [1, 1, 0.4]]]
print(best_of_n(cands, [3.0, 1.0, -0.5]))
