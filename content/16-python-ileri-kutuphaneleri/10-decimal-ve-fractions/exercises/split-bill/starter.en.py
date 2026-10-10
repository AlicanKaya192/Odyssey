from decimal import Decimal


def split_bill(total, n):
    share = (Decimal(total) / n).quantize(Decimal("0.01"))
    return [str(share)] * n

print(split_bill("100.00", 3))
print(split_bill("0.05", 3))
