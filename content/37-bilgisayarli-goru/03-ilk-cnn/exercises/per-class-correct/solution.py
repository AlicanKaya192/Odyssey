import torch


def per_class_correct(predictions, labels, num_classes):
    p = torch.tensor(predictions)
    y = torch.tensor(labels)
    return [((y == c) & (p == c)).sum().item() for c in range(num_classes)]

predictions = [0, 1, 1, 2, 2, 0, 1]
labels = [0, 1, 2, 2, 2, 1, 1]
print(per_class_correct(predictions, labels, 3))
