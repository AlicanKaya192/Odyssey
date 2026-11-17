import statistics


def scale_with_train(values, split):
    mean = statistics.mean(values[:split])
    std = statistics.pstdev(values[:split])
    return [round((v - mean) / std, 3) for v in values]

print(scale_with_train([2.0, 4.0, 6.0, 8.0, 10.0], 3))
