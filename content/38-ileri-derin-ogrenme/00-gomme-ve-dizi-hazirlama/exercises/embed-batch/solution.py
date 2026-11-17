import torch
from torch import nn


def embed_batch(batch_ids, vocab_size, dim):
    torch.manual_seed(0)
    emb = nn.Embedding(vocab_size, dim, padding_idx=0)
    out = emb(torch.tensor(batch_ids))
    zero_rows = int((out.abs().sum(dim=-1) == 0).sum())
    return [list(out.shape), zero_rows, emb.weight.numel()]

batch = [[3, 4, 0, 0], [5, 6, 7, 0]]
print(embed_batch(batch, 10, 4))
