import pickle

import torch
from torch import nn


def load_kind(path):
    torch.load(path, weights_only=False)
    return "ok"


class Note:
    def __init__(self, text):
        self.text = text


torch.save(nn.Linear(2, 1).state_dict(), "weights.pt")
torch.save({"note": Note("hello")}, "odd.pt")
print(load_kind("weights.pt"), load_kind("odd.pt"))
