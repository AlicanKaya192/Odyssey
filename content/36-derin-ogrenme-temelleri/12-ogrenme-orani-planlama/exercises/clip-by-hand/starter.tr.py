import math


def clip_by_norm(grads, max_norm):
    total = 0.0
    return [total, grads]

print(clip_by_norm([[3.0, 4.0]], 1.0))
print(clip_by_norm([[1.0], [2.0, 2.0]], 10.0))
