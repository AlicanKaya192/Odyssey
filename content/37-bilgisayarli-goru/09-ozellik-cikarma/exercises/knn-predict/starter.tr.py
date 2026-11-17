import torch
import torch.nn.functional as F


def knn_predict(memory, memory_labels, queries, k):
    return []

memory = [[1.0, 0.0], [0.9, 0.2], [0.8, -0.1], [0.0, 1.0], [0.1, 0.9], [-0.2, 1.0]]
memory_labels = [0, 0, 0, 1, 1, 1]
print(knn_predict(memory, memory_labels, [[1.0, 0.1], [0.2, 1.0], [0.7, 0.6]], 3))
