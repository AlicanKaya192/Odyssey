import torch
import torch.nn.functional as F


def nearest(vectors, query, k):
    unit = F.normalize(torch.tensor(vectors), dim=1)
    scores = unit @ unit[query]
    scores[query] = -2
    return scores.topk(k).indices.tolist()

vectors = [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0], [0.6, 0.8], [-1.0, -0.2]]
print(nearest(vectors, 0, 2))
print(nearest(vectors, 2, 3))
