def holm_flags(p_values, alpha=0.05):
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    flags = [False] * m
    for k, i in enumerate(order):
        if p_values[i] >= alpha / (m - k):
            break
        flags[i] = True
    return flags


print(holm_flags([0.01, 0.04, 0.03, 0.005]))
