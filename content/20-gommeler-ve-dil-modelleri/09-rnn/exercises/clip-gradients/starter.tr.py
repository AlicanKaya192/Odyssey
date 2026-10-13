import math


def clip_gradients(grads, max_norm):
    return []

print(clip_gradients([3.0, 4.0], 5.0))
print(clip_gradients([6.0, 8.0], 5.0))
print(clip_gradients([0.0, 0.0], 5.0))
