import torch


def confusion(y_true, y_pred, k):
    return []

for row in confusion([0, 0, 1, 1, 2, 2], [0, 1, 1, 1, 2, 0], 3):
    print(row)
