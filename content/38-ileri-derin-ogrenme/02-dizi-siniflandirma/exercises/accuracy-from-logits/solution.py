import torch


def accuracy_from_logits(logits, labels):
    predicted = torch.tensor(logits).argmax(dim=1)
    correct = (predicted == torch.tensor(labels)).sum().item()
    return round(correct / len(labels), 3)

logits = [[2.0, 1.0], [0.0, 3.0], [1.0, -1.0], [0.5, 0.2]]
print(accuracy_from_logits(logits, [0, 1, 1, 0]))
print(accuracy_from_logits(logits, [1, 0, 1, 1]))
