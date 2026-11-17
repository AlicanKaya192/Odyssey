import torch
from torch import nn


def lstm_shapes(input_size, hidden, layers, bidirectional, batch, steps):
    lstm = nn.LSTM(input_size, hidden, num_layers=layers,
                   bidirectional=bidirectional, batch_first=True)
    x = torch.zeros(batch, steps, input_size)
    out, (h, c) = lstm(x)
    return [list(out.shape), list(h.shape), list(c.shape)]

print(lstm_shapes(4, 3, 1, False, 2, 5))
print(lstm_shapes(4, 3, 2, True, 2, 5))
