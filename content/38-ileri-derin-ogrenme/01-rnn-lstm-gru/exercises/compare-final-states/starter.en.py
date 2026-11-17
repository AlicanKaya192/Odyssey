import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence


def compare_final_states(lengths):
    torch.manual_seed(0)
    lstm = nn.LSTM(2, 3, batch_first=True)
    x = torch.randn(len(lengths), max(lengths), 2)
    for i, n in enumerate(lengths):
        x[i, n:] = 0
    # Write your code here
    return []

print(compare_final_states([4, 4, 2]))
print(compare_final_states([3, 1]))
