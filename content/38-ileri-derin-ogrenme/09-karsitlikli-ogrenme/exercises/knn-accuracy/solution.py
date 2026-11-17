import torch
import torch.nn.functional as F


def knn_accuracy(train_vecs, train_labels, test_vecs, test_labels):
    a = F.normalize(torch.tensor(train_vecs), dim=1)
    b = F.normalize(torch.tensor(test_vecs), dim=1)
    pred = torch.tensor(train_labels)[(b @ a.T).argmax(dim=1)]
    return round((pred == torch.tensor(test_labels)).float().mean().item(), 2)

train_vecs = [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]
train_labels = [0, 1, 2]
test_vecs = [[2.0, 0.1], [0.1, 3.0], [-1.0, -0.2], [0.9, 0.8]]
print(knn_accuracy(train_vecs, train_labels, test_vecs, [0, 1, 2, 2]))
