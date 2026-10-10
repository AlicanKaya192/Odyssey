from fractions import Fraction


def add_fractions(items):
    total = Fraction(0)
    for item in items:
        total += Fraction(item)
    return str(total)

print(add_fractions(["1/3", "1/6"]))
print(add_fractions(["1/2", "1/4", "1/8"]))
