import torch


def attention(q, k, v):
    # Kodunu buraya yaz
    return []

q = [[1.0, 0.0]]
k = [[1.0, 0.0], [0.0, 1.0]]
v = [[10.0, 0.0], [0.0, 10.0]]
print(attention(q, k, v))
print(attention([[0.0, 0.0]], k, v))
