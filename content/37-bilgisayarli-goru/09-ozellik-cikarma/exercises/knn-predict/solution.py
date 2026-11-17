import torch
import torch.nn.functional as F


def knn_predict(memory, memory_labels, queries, k):
    m = F.normalize(torch.tensor(memory), dim=1)
    qs = F.normalize(torch.tensor(queries), dim=1)
    nearest = (qs @ m.T).topk(k, dim=1).indices
    labels = torch.tensor(memory_labels)[nearest]
    return [max(set(row), key=row.count) for row in labels.tolist()]

memory = [[1.0, 0.0], [0.9, 0.2], [0.8, -0.1], [0.0, 1.0], [0.1, 0.9], [-0.2, 1.0]]
memory_labels = [0, 0, 0, 1, 1, 1]
print(knn_predict(memory, memory_labels, [[1.0, 0.1], [0.2, 1.0], [0.7, 0.6]], 3))
