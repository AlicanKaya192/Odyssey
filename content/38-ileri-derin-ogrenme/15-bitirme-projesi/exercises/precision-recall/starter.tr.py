import torch


def precision_recall(pred, labels):
    # Ariza sinifi (1) icin [kesinlik, duyarlilik], 2 basamak
    return [0.0, 0.0]

print(precision_recall([1, 1, 0, 0, 1], [1, 0, 0, 1, 1]))
