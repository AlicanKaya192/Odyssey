from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN


def round_price(text, rule):
    return str(round(float(text), 2))

print(round_price("2.665", "up"), round_price("2.665", "even"))
print(round_price("10", "up"))
