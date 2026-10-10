# decimal and fractions

In Python, `0.1 + 0.2` is not exactly `0.3`. This is not a bug; it follows
from how the `float` type stores numbers in the computer. In scientific work
and machine learning the tiny difference does not matter; but in **money**
calculations not even a cent may go missing. This section covers two standard
library modules: `decimal`, which keeps decimal numbers **exact**, and
`fractions`, which keeps fractions exact.

## Why does float surprise you?

```python
from decimal import Decimal

print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(Decimal(0.1))
print(round(2.675, 2))
print(round(0.5), round(1.5), round(2.5))
```

```text
0.30000000000000004 False
0.1000000000000000055511151231257827021181583404541015625
2.67
0 2 2
```

- `float` stores a number as a **binary** fraction. In base two, `0.1` is an
  endlessly repeating fraction (like 1/3 being `0.333...` in base ten); memory
  holds the closest number to it. `Decimal(0.1)` shows that number's real
  value.
- That is why `0.1 + 0.2` comes out with a small leftover and `==` gives
  false.
- `round(2.675, 2)` is `2.67`, not `2.68`: the `2.675` in memory is actually
  slightly smaller.
- `round` rounds halves **to the nearest even** number (banker's rounding):
  `0.5` → `0`, `2.5` → `2`. Not the "five goes up" rule learned at school.

## Decimal: exact numbers in base ten

```python
from decimal import Decimal, InvalidOperation

total = Decimal("0.1") + Decimal("0.2")
print(total, total == Decimal("0.3"))
print(Decimal("1.10") + Decimal("2.20"), Decimal("19.99") * 3)
try:
    Decimal("1.5") + 1.5
except TypeError as error:
    print("TypeError:", error)
try:
    Decimal("abc")
except InvalidOperation:
    print("InvalidOperation")
```

```text
0.3 True
3.30 59.97
TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'
InvalidOperation
```

- `Decimal` stores a number in **base ten**; `0.1` really is `0.1`.
- **Build it from a string:** `Decimal("0.1")`. If you write `Decimal(0.1)`,
  the float's inexact value is copied as it is (the long number above).
- Trailing zeros are kept: `1.10 + 2.20` → `3.30`. Natural for money.
- `Decimal` mixes with `int` (`* 3`) but **not** with `float`: `TypeError`.
  This is deliberate; it stops an inexact float slipping in silently.
- Text that cannot be read raises `InvalidOperation`.

## quantize: rounding to a digit

```python
from decimal import Decimal, ROUND_HALF_UP

cent = Decimal("0.01")
print(Decimal("2.675").quantize(cent))
half = Decimal("2.665")
print(half.quantize(cent), half.quantize(cent, rounding=ROUND_HALF_UP))
print(Decimal("100.00").quantize(Decimal("1")))
print(f"{Decimal('1234.5'):,.2f}")
```

```text
2.68
2.66 2.67
100
1,234.50
```

- **`quantize(Decimal("0.01"))`** rounds the number to the digit of the
  given example (two decimals). Here `2.675` really is `2.675`, so it comes
  out `2.68`; with float it came out `2.67`.
- The default rule is `ROUND_HALF_EVEN` (halves to the even one): `2.675` →
  `2.68` but `2.665` → `2.66`. It is common in banking so that errors cancel
  out over many roundings.
- **`rounding=ROUND_HALF_UP`** is the school "five goes up" rule: `2.665` →
  `2.67`. On an invoice or for tax you write whichever rule applies; it is
  stated in the contract or the regulations.
- f-string formats work with `Decimal` too: a thousands separator and two
  decimals.

## Precision: the context

```python
from decimal import Decimal, getcontext, localcontext

print(getcontext().prec)
print(Decimal(1) / Decimal(3))
with localcontext() as ctx:
    ctx.prec = 5
    print(Decimal(1) / Decimal(3))
print(Decimal(10) / Decimal(3))
```

```text
28
0.3333333333333333333333333333
0.33333
3.333333333333333333333333333
```

- `Decimal` cannot keep infinitely many digits; the context decides how many
  **significant digits** a division computes. The default `prec` is 28.
- **`localcontext()`** opens a context valid only inside the `with` block;
  when the block ends the old setting comes back. Writing
  `getcontext().prec = 5` affects the whole program; library code does not do
  that.
- `prec` is the **total** number of significant digits, not decimal places.
  To round to cents, use `quantize`.

## Splitting money: the lost cent

```python
from decimal import Decimal, ROUND_DOWN

total = Decimal("100.00")
share = (total / 3).quantize(Decimal("0.01"))
print(share, share * 3)
base = (total / 3).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
rest = total - base * 3
cents = int(rest / Decimal("0.01"))
parts = [base + Decimal("0.01") if i < cents else base for i in range(3)]
print(parts, sum(parts))
```

```text
33.33 99.99
[Decimal('33.34'), Decimal('33.33'), Decimal('33.33')] 100.00
```

- When 100 is split three ways and rounded to cents, `33.33 × 3 = 99.99`: a
  cent was lost. `Decimal` computes exactly, but rounding still throws
  information away.
- The right way: round the shares **down** (`ROUND_DOWN`), count the
  remainder (`0.01`) and hand out one cent each to the first shares. The
  total always matches exactly.
- This is what real programs do for instalments and splitting a bill.

## Fraction: exact fractions

```python
from fractions import Fraction

print(Fraction(1, 3) + Fraction(1, 6))
print(Fraction(6, 8), Fraction("0.75"))
f = Fraction(3, 4)
print(f.numerator, f.denominator, float(f))
print(Fraction(0.1))
print(Fraction(0.1).limit_denominator(100))
```

```text
1/2
3/4 3/4
3 4 0.75
3602879701896397/36028797018963968
1/10
```

- `Fraction(numerator, denominator)` keeps a fraction exact and **simplifies
  it automatically**: `6/8` → `3/4`. `1/3 + 1/6` is exactly `1/2`.
- It can be built from a string too: `Fraction("0.75")`.
- The `numerator` and `denominator` attributes; `float(f)` converts to a
  decimal.
- A fraction built from a float carries the float's real (binary) value: a
  huge fraction. `limit_denominator(100)` finds the closest fraction whose
  denominator is at most 100: `1/10`.
- Used where the result must stay exact as a fraction: probability, ratios,
  rhythm in music, measures in a recipe. Odyssey's maths problems also compare
  answers with `Fraction` (`1/2` = `0.5`).

## Which one when?

| Type | For | Watch out |
|---|---|---|
| `float` | science, measurement, ML, charts | fast; `math.isclose` instead of `==` |
| `Decimal` | money, invoices, tax | build from strings; `quantize` + a rounding rule |
| `Fraction` | exact ratios, fractional results | the denominator can grow and slow it down |
| `int` | amounts in cents | `1999` cents = 19.99; careful when dividing |

If floats must be compared, `math.isclose(0.1 + 0.2, 0.3)` → `True`. In a
database, money is usually stored in a `DECIMAL(10, 2)` column or as an
integer number of cents.

## Summary

- `float` is approximate in base two; `0.1 + 0.2 != 0.3`, `round` rounds
  halves to even.
- `Decimal("...")` is built from a string, exact in base ten; it does not mix
  with float.
- `quantize(Decimal("0.01"), rounding=...)` rounds to cents; you choose the
  rule.
- `localcontext()` for temporary precision; `prec` is the number of
  significant digits.
- When splitting money, hand out the remainder; the total must match.
- `Fraction` keeps fractions exact and simplified; `limit_denominator`
  approximates a float with a fraction.
