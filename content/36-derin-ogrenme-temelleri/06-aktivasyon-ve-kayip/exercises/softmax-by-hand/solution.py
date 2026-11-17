import torch


def to_probabilities(logits):
    z = torch.tensor(logits)
    exps = torch.exp(z)
    probs = exps / exps.sum(dim=1, keepdim=True)
    return [[round(v, 3) for v in row] for row in probs.tolist()]

print(to_probabilities([[2.0, 1.0, 0.1]]))
print(to_probabilities([[0.0, 0.0], [3.0, -3.0]]))
