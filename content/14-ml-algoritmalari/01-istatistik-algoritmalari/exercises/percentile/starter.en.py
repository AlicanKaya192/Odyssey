def percentile(values, q):
    s = sorted(values)
    pos = (len(s) - 1) * q / 100
    # Lower and upper neighbour; linear in between.
    return 0.0

data = [7, 1, 3, 9, 4, 6, 2]
for q in (0, 25, 50, 90, 100):
    print(q, percentile(data, q))
