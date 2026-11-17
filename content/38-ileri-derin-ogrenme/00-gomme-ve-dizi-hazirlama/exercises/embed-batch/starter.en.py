import torch
from torch import nn


def embed_batch(batch_ids, vocab_size, dim):
    torch.manual_seed(0)
    # Write your code here
    return []

batch = [[3, 4, 0, 0], [5, 6, 7, 0]]
print(embed_batch(batch, 10, 4))
