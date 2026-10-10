import numpy as np


def add_scores(a, b):
    x = np.array(a, dtype=np.int8).astype(np.int16)
    y = np.array(b, dtype=np.int8).astype(np.int16)
    return (x + y).tolist()

print(add_scores([100, 120], [100, 10]))
