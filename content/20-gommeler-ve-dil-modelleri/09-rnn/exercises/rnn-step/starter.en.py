import numpy as np


def rnn_step(x, h, Wx, Wh, b):
    return []

Wx = [[1.0, 0.0], [0.0, 1.0]]
Wh = [[0.5, 0.0], [0.0, -0.5]]
print(rnn_step([1.0, 0.0], [0.0, 0.0], Wx, Wh, [0.0, 0.0]))
print(rnn_step([1.0, 0.0], [1.0, 1.0], Wx, Wh, [0.0, 0.5]))
