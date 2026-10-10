from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

RULES = {"up": ROUND_HALF_UP, "even": ROUND_HALF_EVEN}


def round_price(text, rule):
    value = Decimal(text).quantize(Decimal("0.01"), rounding=RULES[rule])
    return str(value)

print(round_price("2.665", "up"), round_price("2.665", "even"))
print(round_price("10", "up"))
