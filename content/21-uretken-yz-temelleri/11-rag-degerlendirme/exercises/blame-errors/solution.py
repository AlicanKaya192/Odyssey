def blame(cases, k):
    counts = [0, 0, 0]
    for correct, rank in cases:
        if correct:
            counts[0] += 1
        elif rank is None or rank > k:
            counts[1] += 1
        else:
            counts[2] += 1
    return counts


cases = [[True, 1], [False, None], [False, 2], [False, 5], [True, 3]]
print(blame(cases, 3))
