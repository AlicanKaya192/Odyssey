def simpson_flags(buy_a, n_a, buy_b, n_b):
    pairs = zip(buy_a, n_a, buy_b, n_b)
    every = all(bb / nb > ba / na for ba, na, bb, nb in pairs)
    pooled = sum(buy_b) > sum(buy_a)
    return [every, pooled]


print(simpson_flags([180, 50], [1500, 1000], [22, 52], [170, 1000]))
