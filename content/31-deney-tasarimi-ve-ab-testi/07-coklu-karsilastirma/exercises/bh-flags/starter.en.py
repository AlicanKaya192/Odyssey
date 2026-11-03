def bh_flags(p_values, q=0.05):
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    last = 0
    for k, i in enumerate(order, start=1):
        if p_values[i] > k * q / m:
            break
        last = k
    flags = [False] * m
    for i in order[:last]:
        flags[i] = True
    return flags


print(bh_flags([0.02, 0.035, 0.036, 0.9]))
