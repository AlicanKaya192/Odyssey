import math


def share_se(p, n):
    return round(math.sqrt(p * (1 - p) / n), 4)


print(share_se(0.114, 50))
print(share_se(0.114, 500))
print(share_se(0.5, 100))
