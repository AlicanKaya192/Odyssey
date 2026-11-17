import torch
from torch import nn


def lm_loss(logits, targets):
    # Kodunu buraya yaz
    return 0.0

zeros = [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]]
print(lm_loss(zeros, [[1, 3]]))
sure = [[[8.0, 0.0], [0.0, 8.0]]]
print(lm_loss(sure, [[0, 1]]))
