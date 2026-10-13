import numpy as np


def run_rnn(xs, Wx, Wh, b):
    return []

Wx = [[1.0, 0.0], [0.0, 1.0]]
Wh = [[0.5, 0.5], [-0.5, 0.5]]
b = [0.0, 0.0]
xs = [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]
print(run_rnn(xs, Wx, Wh, b))
print(run_rnn(xs[::-1], Wx, Wh, b))
