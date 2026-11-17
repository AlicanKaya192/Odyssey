import torch


def accuracy_from_logits(logits, labels):
    # Kodunu buraya yaz
    return 0.0

logits = [[2.0, 1.0], [0.0, 3.0], [1.0, -1.0], [0.5, 0.2]]
print(accuracy_from_logits(logits, [0, 1, 1, 0]))
print(accuracy_from_logits(logits, [1, 0, 1, 1]))
