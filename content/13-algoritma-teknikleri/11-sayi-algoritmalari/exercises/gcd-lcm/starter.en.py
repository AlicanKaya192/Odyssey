def gcd_lcm(a, b):
    x, y = a, b
    # Euclid: (x, y) = (y, x % y) until y is zero.
    return x, a * b // x

print(gcd_lcm(1071, 462))
print(gcd_lcm(12, 18))
print(gcd_lcm(7, 1))
