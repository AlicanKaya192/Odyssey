import torch


def linear(x, W, b):
    x, W, b = torch.tensor(x), torch.tensor(W), torch.tensor(b)
    return (x @ W.T + b).tolist()

x = [[1.0, 2.0], [0.0, 1.0], [3.0, -1.0]]
W = [[1.0, 1.0], [2.0, 0.0], [0.0, -1.0]]
b = [0.5, 0.0, 1.0]
for row in linear(x, W, b):
    print(row)
