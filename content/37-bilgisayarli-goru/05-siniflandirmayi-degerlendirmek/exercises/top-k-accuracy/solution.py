import torch


def top_k_accuracy(logits, labels, k):
    top = torch.tensor(logits).topk(k, dim=1).indices
    hit = (top == torch.tensor(labels)[:, None]).any(dim=1)
    return round(hit.float().mean().item(), 3)

logits = [[0.1, 0.5, 0.4], [0.7, 0.2, 0.1], [0.3, 0.35, 0.4], [0.2, 0.5, 0.3]]
labels = [2, 0, 1, 0]
print(top_k_accuracy(logits, labels, 1))
print(top_k_accuracy(logits, labels, 2))
print(top_k_accuracy(logits, labels, 3))
