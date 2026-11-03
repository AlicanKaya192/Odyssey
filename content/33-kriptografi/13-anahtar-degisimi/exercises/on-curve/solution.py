def on_curve(x, y, a, b, p):
    return (y * y - (x ** 3 + a * x + b)) % p == 0

print(on_curve(0, 2, 1, 4, 97))
print(on_curve(1, 43, 1, 4, 97))
print(on_curve(1, 44, 1, 4, 97))
