## Decimal

| Code | What it does |
|---|---|
| `Decimal("19.99")` | an exact number from a string (the right way) |
| `Decimal(0.1)` | copies the float's inexact value (do not) |
| `x.quantize(Decimal("0.01"))` | round to two decimals |
| `rounding=ROUND_HALF_UP` | "five goes up" |
| `rounding=ROUND_HALF_EVEN` | halves to even (the default) |
| `rounding=ROUND_DOWN` | cut towards zero |
| `getcontext().prec` | the number of significant digits (28) |
| `with localcontext() as ctx:` | a temporary context |
| `x.normalize()` | drop trailing zeros |
| `f"{x:,.2f}"` | format |

## Fraction

| Code | What it does |
|---|---|
| `Fraction(3, 4)` | 3/4 |
| `Fraction("0.75")` | from a string |
| `f.numerator`, `f.denominator` | numerator, denominator |
| `float(f)` | to a decimal |
| `Fraction(x).limit_denominator(n)` | the closest fraction with a denominator of at most n |

## Errors

| Error | Cause |
|---|---|
| `TypeError: unsupported operand type(s)` | `Decimal` mixed with `float` |
| `InvalidOperation` | unreadable text like `Decimal("abc")` |
| `0.30000000000000004` | money computed with float |
| `99.99` (instead of 100) | the leftover cent was not handed out after dividing and rounding |

## Rules

- Money is kept with `Decimal` or as an `int` number of cents, not with `float`.
- Float comparison with `math.isclose(a, b)`.
- The rounding rule in one function; intermediate results are not rounded.
