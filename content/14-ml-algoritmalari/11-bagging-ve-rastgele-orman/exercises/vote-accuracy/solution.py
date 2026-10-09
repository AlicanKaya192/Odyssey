from math import comb


def vote_accuracy(n, p):
    total = 0.0
    for k in range(n // 2 + 1, n + 1):
        total += comb(n, k) * p ** k * (1 - p) ** (n - k)
    return round(total, 3)

for n in (1, 5, 25, 101):
    print(n, vote_accuracy(n, 0.6))
print(vote_accuracy(25, 0.45))
