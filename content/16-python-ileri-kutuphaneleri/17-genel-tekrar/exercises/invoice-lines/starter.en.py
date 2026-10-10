from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


def invoice_total(rows, rate):
    total = sum(float(price) * qty for _, price, qty in rows)
    return str(round(total * (1 + float(rate)), 2))

print(invoice_total([["pen", "1.15", 3], ["book", "12.49", 2]], "0.20"))
