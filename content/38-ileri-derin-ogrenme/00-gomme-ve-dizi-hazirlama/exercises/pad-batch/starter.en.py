import torch
from torch.nn.utils.rnn import pad_sequence


def pad_batch(seqs):
    # Write your code here
    return [[], []]

padded, lengths = pad_batch([[4, 2, 3], [5], [7, 7]])
print(padded)
print(lengths)
