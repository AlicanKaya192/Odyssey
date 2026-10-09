import math


def bic_choice(logliks, n):
    bics = []
    # k = 1, 2, ...: p = 3k - 1
    return bics, 1

lls = [-1134.9, -1064.4, -1063.8, -1062.0, -1058.9]
bics, best = bic_choice(lls, 500)
print(bics)
print(best)
