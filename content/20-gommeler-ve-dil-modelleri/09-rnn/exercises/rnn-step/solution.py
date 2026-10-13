import numpy as np


def rnn_step(x, h, Wx, Wh, b):
    z = np.array(x) @ np.array(Wx) + np.array(h) @ np.array(Wh) + np.array(b)
    return np.tanh(z).round(3).tolist()

Wx = [[1.0, 0.0], [0.0, 1.0]]
Wh = [[0.5, 0.0], [0.0, -0.5]]
print(rnn_step([1.0, 0.0], [0.0, 0.0], Wx, Wh, [0.0, 0.0]))
print(rnn_step([1.0, 0.0], [1.0, 1.0], Wx, Wh, [0.0, 0.5]))
