import torch
from torchvision.ops import box_iou


def best_matches(predicted, truth):
    return []

truth = [[10, 10, 20, 20], [0, 0, 6, 6]]
predicted = [[11, 10, 21, 20], [1, 1, 6, 7], [25, 25, 30, 30]]
for row in best_matches(predicted, truth):
    print(row)
