import torch


def pad_sequences(seqs, pad=0):
    # [en uzuna dolgulu ic ice liste, uzunluklar]
    return [[], []]

padded, lengths = pad_sequences([[5, 3], [7], [1, 2, 4]])
for row in padded:
    print(row)
print(lengths)
