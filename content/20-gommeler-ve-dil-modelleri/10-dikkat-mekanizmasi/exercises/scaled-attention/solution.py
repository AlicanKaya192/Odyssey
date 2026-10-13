import numpy as np


def attention(query, keys, values):
    query, keys, values = np.array(query), np.array(keys), np.array(values)
    scores = keys @ query / np.sqrt(len(query))
    weights = np.exp(scores - scores.max())
    weights = weights / weights.sum()
    return (weights @ values).round(2).tolist()

keys = [[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]]
values = [[10.0], [20.0], [30.0]]
print(attention([0.0, 2.0], keys, values))
print(attention([0.0, 0.0], keys, values))
