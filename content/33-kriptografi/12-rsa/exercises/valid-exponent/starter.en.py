import math


def valid_exponent(e, phi):
    return e % 2 == 1

print(valid_exponent(17, 3120))
print(valid_exponent(15, 3120))
print(valid_exponent(1, 3120))
