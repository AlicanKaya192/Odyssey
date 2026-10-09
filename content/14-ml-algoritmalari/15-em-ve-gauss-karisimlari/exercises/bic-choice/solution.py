import math


def bic_choice(logliks, n):
    bics = []
    for k, ll in enumerate(logliks, start=1):
        p = 3 * k - 1
        bics.append(round(p * math.log(n) - 2 * ll, 1))
    best = bics.index(min(bics)) + 1
    return bics, best

lls = [-1134.9, -1064.4, -1063.8, -1062.0, -1058.9]
bics, best = bic_choice(lls, 500)
print(bics)
print(best)
