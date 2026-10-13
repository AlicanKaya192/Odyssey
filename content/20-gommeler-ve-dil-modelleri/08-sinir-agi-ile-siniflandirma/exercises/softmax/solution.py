import math


def softmax(z):
    top = max(z)
    exps = [math.exp(v - top) for v in z]
    total = sum(exps)
    return [round(e / total, 3) for e in exps]

print(softmax([2.0, 1.0, 0.1]))
print(softmax([1000.0, 1000.0]))
