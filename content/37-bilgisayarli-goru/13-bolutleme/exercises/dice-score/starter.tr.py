import torch


def dice(predicted, truth, c):
    return 0.0

truth = [[0, 1, 1], [0, 1, 1], [0, 0, 0]]
print(dice([[0, 1, 1], [0, 1, 0], [0, 0, 0]], truth, 1))
print(dice([[0, 0, 0], [0, 0, 0], [0, 0, 0]], truth, 1))
print(dice(truth, truth, 2))
