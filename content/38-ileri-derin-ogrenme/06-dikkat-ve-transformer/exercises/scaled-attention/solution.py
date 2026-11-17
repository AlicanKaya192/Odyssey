import torch


def attention(q, k, v):
    q, k, v = torch.tensor(q), torch.tensor(k), torch.tensor(v)
    scores = q @ k.T / q.shape[-1] ** 0.5
    weights = torch.softmax(scores, dim=-1)
    return [[round(x, 3) for x in row] for row in (weights @ v).tolist()]

q = [[1.0, 0.0]]
k = [[1.0, 0.0], [0.0, 1.0]]
v = [[10.0, 0.0], [0.0, 10.0]]
print(attention(q, k, v))
print(attention([[0.0, 0.0]], k, v))
