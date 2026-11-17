import torch


def precision_recall(pred, labels):
    # [precision, recall] for the fault class (1), 2 places
    return [0.0, 0.0]

print(precision_recall([1, 1, 0, 0, 1], [1, 0, 0, 1, 1]))
