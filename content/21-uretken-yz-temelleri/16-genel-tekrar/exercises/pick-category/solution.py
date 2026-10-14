def pick(probs, us):
    result = []
    for u in us:
        total = 0.0
        for i, p in enumerate(probs):
            total += p
            if u < total:
                result.append(i)
                break
    return result


print(pick([0.2, 0.5, 0.3], [0.1, 0.65, 0.95]))
