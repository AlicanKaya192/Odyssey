def egcd(a, b):
    if b == 0:
        return [a, 1, 0]
    g, x, y = egcd(b, a % b)
    return [g, y, x - (a // b) * y]


def inverse(a, n):
    g, x, y = egcd(a, n)
    if g != 1:
        return None
    return x % n

print(inverse(3, 11))
print(inverse(17, 3120))
print(inverse(4, 8))
