from decimal import Decimal, ROUND_DOWN

CENT = Decimal("0.01")


def split_bill(total, n):
    amount = Decimal(total)
    base = (amount / n).quantize(CENT, rounding=ROUND_DOWN)
    cents = int((amount - base * n) / CENT)
    return [str(base + CENT) if i < cents else str(base) for i in range(n)]

print(split_bill("100.00", 3))
print(split_bill("0.05", 3))
