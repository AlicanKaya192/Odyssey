import torch


def precision_recall(pred, labels):
    pred, labels = torch.tensor(pred), torch.tensor(labels)
    tp = ((pred == 1) & (labels == 1)).sum().item()
    precision = tp / max(1, (pred == 1).sum().item())
    recall = tp / max(1, (labels == 1).sum().item())
    return [round(precision, 2), round(recall, 2)]

print(precision_recall([1, 1, 0, 0, 1], [1, 0, 0, 1, 1]))
