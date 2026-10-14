def count_trainable(sizes, layers):
    return sum(sizes[i] * sizes[i + 1] + sizes[i + 1] for i in layers)


print(count_trainable([64, 32, 10], [0, 1]))
print(count_trainable([64, 32, 10], [1]))
