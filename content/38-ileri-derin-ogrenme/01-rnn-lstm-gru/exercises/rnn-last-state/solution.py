import torch


def rnn_last_state(xs, w_ih, w_hh):
    w_ih, w_hh = torch.tensor(w_ih), torch.tensor(w_hh)
    h = torch.zeros(w_ih.shape[0])
    for x in torch.tensor(xs):
        h = torch.tanh(x @ w_ih.T + h @ w_hh.T)
    return [round(v, 3) for v in h.tolist()]

xs = [[1.0, 0.0], [0.0, 1.0]]
w_ih = [[0.5, 0.0], [0.0, 0.5]]
w_hh = [[0.0, 0.0], [0.0, 0.0]]
print(rnn_last_state(xs, w_ih, w_hh))
print(rnn_last_state(xs, w_ih, [[1.0, 0.0], [0.0, 1.0]]))
