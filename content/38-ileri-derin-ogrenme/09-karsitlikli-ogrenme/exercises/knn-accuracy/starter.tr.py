import torch
import torch.nn.functional as F


def knn_accuracy(train_vecs, train_labels, test_vecs, test_labels):
    # Kodunu buraya yaz
    return 0.0

train_vecs = [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]
train_labels = [0, 1, 2]
test_vecs = [[2.0, 0.1], [0.1, 3.0], [-1.0, -0.2], [0.9, 0.8]]
print(knn_accuracy(train_vecs, train_labels, test_vecs, [0, 1, 2, 2]))
