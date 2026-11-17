import torch


def standardize(rows):
    x = torch.tensor(rows)
    return x.tolist()

for row in standardize([[1.0, 10.0], [3.0, 30.0], [5.0, 20.0]]):
    print(row)
