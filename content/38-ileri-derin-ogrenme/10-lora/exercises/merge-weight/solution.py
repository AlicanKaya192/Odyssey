import torch


def merge_weight(W, A, B, alpha):
    W, A, B = torch.tensor(W), torch.tensor(A), torch.tensor(B)
    merged = W + (alpha / A.shape[0]) * B @ A
    return [[round(v, 3) for v in row] for row in merged.tolist()]

W = [[1.0, 0.0], [0.0, 1.0]]
A = [[1.0, 2.0]]
B = [[1.0], [0.0]]
print(merge_weight(W, A, B, 1.0))
