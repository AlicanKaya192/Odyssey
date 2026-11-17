import torch


def per_class_correct(predictions, labels, num_classes):
    return []

predictions = [0, 1, 1, 2, 2, 0, 1]
labels = [0, 1, 2, 2, 2, 1, 1]
print(per_class_correct(predictions, labels, 3))
