def make_windows(values, size):
    xs = [values[i:i + size] for i in range(len(values) - size)]
    ys = [values[i + size] for i in range(len(values) - size)]
    return [xs, ys]

xs, ys = make_windows([1, 2, 3, 4, 5], 2)
print(xs)
print(ys)
