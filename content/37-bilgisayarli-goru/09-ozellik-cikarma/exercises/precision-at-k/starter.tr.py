import torch
import torch.nn.functional as F


def precision_at_k(vectors, labels, k):
    return 0.0

vectors = [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0], [0.1, 0.9], [0.8, 0.6]]
labels = [0, 0, 1, 1, 0]
print(precision_at_k(vectors, labels, 1))
print(precision_at_k(vectors, labels, 2))
