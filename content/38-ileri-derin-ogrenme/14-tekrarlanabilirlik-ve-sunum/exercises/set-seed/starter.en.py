import random
import numpy as np
import torch
from torch import nn


def set_seed(seed):
    # Fix the random, numpy and torch seeds
    pass


def same_seed(seed_a, seed_b):
    set_seed(seed_a)
    a = nn.Linear(4, 2)
    set_seed(seed_b)
    b = nn.Linear(4, 2)
    return torch.equal(a.weight, b.weight)

print(same_seed(0, 0), same_seed(0, 1))
