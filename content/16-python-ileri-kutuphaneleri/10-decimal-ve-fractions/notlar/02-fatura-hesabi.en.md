On an invoice, rounding the tax **on every line** and rounding it **once on
the total** can give different results. Which one applies is written in the
regulations or the contract; the program's job is to keep the rule in one
place.

```python
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
VAT = Decimal("0.20")
lines = [("pen", "1.15", 3), ("book", "12.49", 2), ("bag", "7.33", 1)]


def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


net = sum(Decimal(price) * qty for _, price, qty in lines)
per_line = sum(money(Decimal(price) * qty * VAT) for _, price, qty in lines)
on_total = money(net * VAT)
print("net:", net)
print("tax per line:", per_line)
print("tax on total:", on_total)
print("total:", net + on_total)
```

```text
net: 35.76
tax per line: 7.16
tax on total: 7.15
total: 42.91
```

## What happened?

- The line taxes are `0.69`, `4.996` and `1.466`. Rounded line by line:
  `0.69 + 5.00 + 1.47 = 7.16`.
- Computed once on the total `35.76`: `7.152` → `7.15`. A one-cent difference.
- Either can be "right"; what is wrong is using one in one part of the program
  and the other elsewhere. If the invoice screen says 7.16 and the accounting
  report says 7.15, the books do not balance.

## Good habits

- **Rounding in one function** (`money`): if the rule changes, one line
  changes.
- **Prices arrive as text** (`"1.15"`): text is read from CSV, forms or the
  database and turned straight into `Decimal`; no `float` in between.
- **Intermediate results are not rounded**; only the result that is shown or
  stored is (unless the rule says to round per line).
- `sum()` works on a list of `Decimal` too; the start value `0` (an int) is
  no problem.
