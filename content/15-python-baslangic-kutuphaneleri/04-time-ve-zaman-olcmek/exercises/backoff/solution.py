def backoff(n, base, cap):
    return [min(cap, base * 2 ** i) for i in range(n)]

print(backoff(5, 1, 10))
print(backoff(4, 0.5, 100))
