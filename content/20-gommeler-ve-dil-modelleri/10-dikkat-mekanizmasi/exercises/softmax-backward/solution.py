def softmax_backward(a, da):
    dot = sum(x * y for x, y in zip(a, da))
    return [round(x * (y - dot), 4) for x, y in zip(a, da)]

grad = softmax_backward([0.5, 0.3, 0.2], [1.0, 0.0, -1.0])
print(grad)
print(abs(sum(grad)) < 1e-9)
