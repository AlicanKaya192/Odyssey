import torch


def result_shape(shape_a, shape_b):
    return []

print(result_shape([3, 2], [2]))
print(result_shape([3, 1], [1, 4]))
print(result_shape([3, 2], [3]))
