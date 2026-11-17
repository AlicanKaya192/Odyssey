import torch


def class_iou(predicted, truth, num_classes):
    return []

truth = [[0, 0, 1, 1], [0, 0, 1, 1], [2, 2, 0, 0], [2, 2, 0, 0]]
predicted = [[0, 0, 1, 1], [0, 1, 1, 1], [2, 0, 0, 0], [0, 0, 0, 0]]
print(class_iou(predicted, truth, 3))
print(class_iou(predicted, truth, 4))
