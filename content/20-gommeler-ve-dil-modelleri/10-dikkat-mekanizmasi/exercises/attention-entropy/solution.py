import math


def attention_entropy(weights):
    total = 0.0
    for w in weights:
        if w > 0:
            total -= w * math.log2(w)
    return round(total, 3)

print(attention_entropy([1.0, 0.0, 0.0, 0.0]))
print(attention_entropy([0.25, 0.25, 0.25, 0.25]))
print(attention_entropy([0.11, 0.42, 0.24, 0.23]))
