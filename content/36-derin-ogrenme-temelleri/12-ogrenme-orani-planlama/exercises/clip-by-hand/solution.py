import math


def clip_by_norm(grads, max_norm):
    total = math.sqrt(sum(v * v for g in grads for v in g))
    scale = max_norm / total if total > max_norm else 1.0
    clipped = [[round(v * scale, 4) for v in g] for g in grads]
    return [round(total, 4), clipped]

print(clip_by_norm([[3.0, 4.0]], 1.0))
print(clip_by_norm([[1.0], [2.0, 2.0]], 10.0))
