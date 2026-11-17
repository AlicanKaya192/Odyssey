def shift_windows(ids, size):
    xs = [ids[i:i + size] for i in range(len(ids) - size)]
    ys = [ids[i + 1:i + size + 1] for i in range(len(ids) - size)]
    return [xs, ys]

xs, ys = shift_windows([1, 2, 3, 4, 5], 3)
print(xs)
print(ys)
