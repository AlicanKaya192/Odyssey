import math


def clip_gradients(grads, max_norm):
    norm = math.sqrt(sum(g * g for g in grads))
    if norm <= max_norm:
        return [round(g, 3) for g in grads]
    return [round(g * max_norm / norm, 3) for g in grads]

print(clip_gradients([3.0, 4.0], 5.0))
print(clip_gradients([6.0, 8.0], 5.0))
print(clip_gradients([0.0, 0.0], 5.0))
