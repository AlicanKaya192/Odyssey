import torch


def masked_mean(vectors, mask):
    x = torch.tensor(vectors)
    m = torch.tensor(mask, dtype=torch.float32).unsqueeze(-1)
    mean = (x * m).sum(dim=1) / m.sum(dim=1)
    return mean.round(decimals=3).tolist()

vectors = [[[1.0, 2.0], [3.0, 4.0], [0.0, 0.0]],
           [[2.0, 2.0], [0.0, 0.0], [0.0, 0.0]]]
mask = [[1, 1, 0], [1, 0, 0]]
print(masked_mean(vectors, mask))
