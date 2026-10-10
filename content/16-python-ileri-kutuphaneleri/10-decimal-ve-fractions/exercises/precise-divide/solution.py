from decimal import Decimal, getcontext, localcontext


def precise_divide(a, b, digits):
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(a) / Decimal(b))

print(precise_divide("1", "7", 5))
print(precise_divide("2", "3", 3))
print(getcontext().prec)
