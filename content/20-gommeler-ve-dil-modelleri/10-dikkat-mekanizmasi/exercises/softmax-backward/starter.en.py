def softmax_backward(a, da):
    return []

grad = softmax_backward([0.5, 0.3, 0.2], [1.0, 0.0, -1.0])
print(grad)
print(abs(sum(grad)) < 1e-9)
