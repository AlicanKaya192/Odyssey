import torch
from torch import nn


def lm_loss(logits, targets):
    logits = torch.tensor(logits)
    targets = torch.tensor(targets)
    vocab = logits.shape[-1]
    loss = nn.functional.cross_entropy(logits.reshape(-1, vocab), targets.reshape(-1))
    return round(loss.item(), 3)

zeros = [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]]
print(lm_loss(zeros, [[1, 3]]))
sure = [[[8.0, 0.0], [0.0, 8.0]]]
print(lm_loss(sure, [[0, 1]]))
