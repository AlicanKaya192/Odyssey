import torch


def rnn_last_state(xs, w_ih, w_hh):
    # Write your code here
    return []

xs = [[1.0, 0.0], [0.0, 1.0]]
w_ih = [[0.5, 0.0], [0.0, 0.5]]
w_hh = [[0.0, 0.0], [0.0, 0.0]]
print(rnn_last_state(xs, w_ih, w_hh))
print(rnn_last_state(xs, w_ih, [[1.0, 0.0], [0.0, 1.0]]))
