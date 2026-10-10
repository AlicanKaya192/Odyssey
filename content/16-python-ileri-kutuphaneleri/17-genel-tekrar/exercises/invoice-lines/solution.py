from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass
class Line:
    name: str
    price: Decimal
    qty: int


def invoice_total(rows, rate):
    lines = [Line(name, Decimal(price), qty) for name, price, qty in rows]
    net = sum((line.price * line.qty for line in lines), Decimal(0))
    gross = net * (1 + Decimal(rate))
    return str(gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

print(invoice_total([["pen", "1.15", 3], ["book", "12.49", 2]], "0.20"))
