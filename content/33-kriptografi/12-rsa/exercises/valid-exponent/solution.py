import math


def valid_exponent(e, phi):
    return 1 < e < phi and math.gcd(e, phi) == 1

print(valid_exponent(17, 3120))
print(valid_exponent(15, 3120))
print(valid_exponent(1, 3120))
