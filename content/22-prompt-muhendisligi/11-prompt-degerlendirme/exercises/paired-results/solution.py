def paired(ok1, ok2):
    only1 = sum(a and not b for a, b in zip(ok1, ok2))
    only2 = sum(b and not a for a, b in zip(ok1, ok2))
    both = sum(a and b for a, b in zip(ok1, ok2))
    neither = len(ok1) - only1 - only2 - both
    return [only1, only2, both, neither]


print(paired([True, True, False, False, True],
             [True, False, True, True, False]))
