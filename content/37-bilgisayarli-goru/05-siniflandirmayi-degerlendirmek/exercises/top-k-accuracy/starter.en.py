import torch


def top_k_accuracy(logits, labels, k):
    return 0.0

logits = [[0.1, 0.5, 0.4], [0.7, 0.2, 0.1], [0.3, 0.35, 0.4], [0.2, 0.5, 0.3]]
labels = [2, 0, 1, 0]
print(top_k_accuracy(logits, labels, 1))
print(top_k_accuracy(logits, labels, 2))
print(top_k_accuracy(logits, labels, 3))
