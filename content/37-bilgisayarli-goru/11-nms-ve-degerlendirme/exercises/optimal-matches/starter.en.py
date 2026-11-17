import torch
from scipy.optimize import linear_sum_assignment
from torchvision.ops import box_iou


def optimal_matches(predicted, truth, threshold):
    return []

truth = [[0, 0, 10, 10], [4, 0, 14, 10]]
predicted = [[3, 0, 13, 10], [5, 0, 15, 10]]
print(optimal_matches(predicted, truth, 0.5))
print(optimal_matches([[40, 40, 50, 50]] + predicted, truth, 0.5))
