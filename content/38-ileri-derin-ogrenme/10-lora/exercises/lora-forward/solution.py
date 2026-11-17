import torch


def lora_forward(x, W, b, A, B, alpha):
    x, W, b, A, B = (torch.tensor(v) for v in (x, W, b, A, B))
    scale = alpha / A.shape[0]
    out = x @ W.T + b + (x @ A.T @ B.T) * scale
    return [[round(v, 3) for v in row] for row in out.tolist()]

x = [[1.0, 2.0]]
W = [[1.0, 0.0], [0.0, 1.0]]
b = [0.0, 0.0]
A = [[1.0, 1.0]]
B = [[0.5], [0.0]]
print(lora_forward(x, W, b, A, B, 2.0))
