import torch
from torch.nn.utils.rnn import pad_sequence


def pad_batch(seqs):
    tensors = [torch.tensor(s) for s in seqs]
    padded = pad_sequence(tensors, batch_first=True, padding_value=0)
    return [padded.tolist(), [len(s) for s in seqs]]

padded, lengths = pad_batch([[4, 2, 3], [5], [7, 7]])
print(padded)
print(lengths)
