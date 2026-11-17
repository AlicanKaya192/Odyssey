import torch


def standardize(rows):
    x = torch.tensor(rows)
    scaled = (x - x.mean(dim=0)) / x.std(dim=0)
    return [[round(v, 3) for v in row] for row in scaled.tolist()]

print(standardize([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]]))
print(standardize([[0.0, 4.0], [2.0, 0.0]]))
