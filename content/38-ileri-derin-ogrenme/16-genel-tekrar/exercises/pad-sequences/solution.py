import torch


def pad_sequences(seqs, pad=0):
    longest = max(len(s) for s in seqs)
    padded = torch.full((len(seqs), longest), pad)
    for i, s in enumerate(seqs):
        padded[i, :len(s)] = torch.tensor(s)
    return [padded.tolist(), [len(s) for s in seqs]]

padded, lengths = pad_sequences([[5, 3], [7], [1, 2, 4]])
for row in padded:
    print(row)
print(lengths)
