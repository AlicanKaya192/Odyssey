import torch


def mean_iou(predicted, truth, num_classes):
    return 0.0

truth = [[0, 0, 1], [0, 1, 1], [2, 2, 0]]
predicted = [[0, 0, 1], [0, 0, 1], [2, 0, 0]]
print(mean_iou(predicted, truth, 3))
print(mean_iou(predicted, truth, 5))
