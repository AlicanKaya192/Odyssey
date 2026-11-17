import torch


def pixel_accuracy(predicted, truth):
    return 0.0

truth = [[0, 0, 1], [0, 2, 2], [1, 1, 0]]
print(pixel_accuracy([[0, 0, 1], [0, 2, 0], [1, 0, 0]], truth))
print(pixel_accuracy([[0, 0, 0], [0, 0, 0], [0, 0, 0]], truth))
