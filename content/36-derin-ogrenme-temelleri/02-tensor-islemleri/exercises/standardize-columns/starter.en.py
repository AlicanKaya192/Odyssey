import torch


def standardize(rows):
    x = torch.tensor(rows)
    return x.tolist()

print(standardize([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]]))
print(standardize([[0.0, 4.0], [2.0, 0.0]]))
