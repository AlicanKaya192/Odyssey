import math

X = [[1.0, 2.0], [2.0, -1.0], [-1.0, 0.5]]
Y = [1, 0, 1]


def loss(w):
    total = 0.0
    for x, y in zip(X, Y):
        p = 1 / (1 + math.exp(-(w[0] * x[0] + w[1] * x[1])))
        total -= math.log(p if y == 1 else 1 - p)
    return total / len(X)


def numeric_gradient(w, eps):
    return []

print(numeric_gradient([0.5, -0.2], 1e-5))
print(numeric_gradient([0.0, 0.0], 1e-5))
