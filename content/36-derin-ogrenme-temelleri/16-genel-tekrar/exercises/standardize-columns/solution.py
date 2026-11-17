import torch


def standardize(rows):
    x = torch.tensor(rows)
    z = (x - x.mean(dim=0)) / x.std(dim=0, unbiased=False)
    return [[round(v, 2) + 0.0 for v in row] for row in z.tolist()]

for row in standardize([[1.0, 10.0], [3.0, 30.0], [5.0, 20.0]]):
    print(row)
