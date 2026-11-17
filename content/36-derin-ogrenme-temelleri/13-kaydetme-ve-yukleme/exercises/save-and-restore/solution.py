import torch
from torch import nn


def make(seed):
    torch.manual_seed(seed)
    return nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))


def restore_matches(seed_a, seed_b):
    original = make(seed_a)
    torch.save(original.state_dict(), "weights.pt")
    restored = make(seed_b)
    x = torch.ones(2, 4)
    before = torch.equal(original(x), restored(x))
    restored.load_state_dict(torch.load("weights.pt", weights_only=True))
    after = torch.equal(original(x), restored(x))
    return [before, after]

print(restore_matches(0, 1))
