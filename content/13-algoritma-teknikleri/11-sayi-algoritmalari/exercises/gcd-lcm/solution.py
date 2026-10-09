def gcd_lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return x, a * b // x

print(gcd_lcm(1071, 462))
print(gcd_lcm(12, 18))
print(gcd_lcm(7, 1))
