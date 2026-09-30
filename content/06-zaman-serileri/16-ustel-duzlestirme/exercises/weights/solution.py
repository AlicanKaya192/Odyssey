def weights(alpha, n):
    return [alpha * (1 - alpha) ** k for k in range(n)]


print([round(w, 3) for w in weights(0.3, 6)])
print(round(sum(weights(0.3, 10)), 3))
print([round(w, 3) for w in weights(0.9, 3)])


def needed(alpha):
    total = 0.0
    k = 0
    while total <= 0.95:
        total += alpha * (1 - alpha) ** k
        k += 1
    return k


print([needed(alpha) for alpha in (0.1, 0.3, 0.9)])
