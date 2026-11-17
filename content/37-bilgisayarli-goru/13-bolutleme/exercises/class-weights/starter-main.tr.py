import torch
from dl_data import make_scenes


def class_weights(n, seed):
    return []

print(class_weights(100, 7))
print(class_weights(50, 3))
