import torch


def accuracy(logits, labels):
    predictions = torch.tensor(logits).argmax(dim=1)
    correct = (predictions == torch.tensor(labels)).float().mean()
    return round(correct.item(), 3)

logits = [[2.0, 0.5, 0.1], [0.2, 0.1, 3.0], [1.0, 2.0, 0.0], [0.3, 0.2, 0.1]]
print(accuracy(logits, [0, 2, 1, 1]))
print(accuracy(logits, [0, 2, 1, 0]))
