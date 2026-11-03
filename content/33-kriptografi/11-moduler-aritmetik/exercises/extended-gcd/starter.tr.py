def egcd(a, b):
    if b == 0:
        return [a, 0, 1]
    g, x, y = egcd(b, a % b)
    return [g, y, x - (a // b) * y]

g, x, y = egcd(3, 11)
print(g, x, y)
print(3 * x + 11 * y)
g, x, y = egcd(240, 46)
print(g, 240 * x + 46 * y)
