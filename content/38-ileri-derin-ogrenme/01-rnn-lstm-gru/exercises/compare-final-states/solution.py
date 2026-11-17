import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence


def compare_final_states(lengths):
    torch.manual_seed(0)
    lstm = nn.LSTM(2, 3, batch_first=True)
    x = torch.randn(len(lengths), max(lengths), 2)
    for i, n in enumerate(lengths):
        x[i, n:] = 0
    out, (h, c) = lstm(x)
    packed = pack_padded_sequence(x, torch.tensor(lengths), batch_first=True,
                                  enforce_sorted=False)
    _, (h_p, c_p) = lstm(packed)
    plain, with_pack = [], []
    for i, n in enumerate(lengths):
        plain.append(torch.allclose(h[0, i], out[i, n - 1]))
        with_pack.append(torch.allclose(h_p[0, i], out[i, n - 1]))
    return [plain, with_pack]

print(compare_final_states([4, 4, 2]))
print(compare_final_states([3, 1]))
