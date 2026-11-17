import torch


def pairwise_sq_dist(a, b):
    a, b = torch.tensor(a), torch.tensor(b)
    return ((a[:, None, :] - b[None, :, :]) ** 2).sum(dim=-1).long().tolist()

print(pairwise_sq_dist([[0.0, 0.0], [1.0, 2.0]], [[1.0, 0.0], [3.0, 2.0]]))
