MULTS = 0


def karatsuba(x, y):
    global MULTS
    if x < 10 or y < 10:
        MULTS += 1
        return x * y
    half = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10 ** half)
    c, d = divmod(y, 10 ** half)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    middle = karatsuba(a + b, c + d) - ac - bd
    return ac * 10 ** (2 * half) + middle * 10 ** half + bd


def count_mults(x, y):
    global MULTS
    MULTS = 0
    karatsuba(x, y)
    return MULTS


print(karatsuba(1234, 5678))
print(karatsuba(31415926535, 27182818284) == 31415926535 * 27182818284)
print(count_mults(12345678, 87654321))
