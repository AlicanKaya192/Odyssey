## Decimal

| Yazım | Ne yapar |
|---|---|
| `Decimal("19.99")` | metinden tam sayı (doğru yol) |
| `Decimal(0.1)` | float'ın hatalı değerini kopyalar (yapma) |
| `x.quantize(Decimal("0.01"))` | iki ondalığa yuvarla |
| `rounding=ROUND_HALF_UP` | "beş yukarı" |
| `rounding=ROUND_HALF_EVEN` | yarımda çifte (varsayılan) |
| `rounding=ROUND_DOWN` | sıfıra doğru kes |
| `getcontext().prec` | anlamlı basamak sayısı (28) |
| `with localcontext() as ctx:` | geçici bağlam |
| `x.normalize()` | sondaki sıfırları at |
| `f"{x:,.2f}"` | biçimlendir |

## Fraction

| Yazım | Ne yapar |
|---|---|
| `Fraction(3, 4)` | 3/4 |
| `Fraction("0.75")` | metinden |
| `f.numerator`, `f.denominator` | pay, payda |
| `float(f)` | ondalığa |
| `Fraction(x).limit_denominator(n)` | paydası en fazla n olan en yakın kesir |

## Hatalar

| Hata | Sebep |
|---|---|
| `TypeError: unsupported operand type(s)` | `Decimal` ile `float` karıştı |
| `InvalidOperation` | `Decimal("abc")` gibi okunamayan metin |
| `0.30000000000000004` | float ile para hesabı |
| `99.99` (100 yerine) | bölüp yuvarlayınca kalan kuruş dağıtılmadı |

## Kurallar

- Para `Decimal` ile ya da kuruş cinsinden `int` ile tutulur, `float` ile değil.
- Float karşılaştırması `math.isclose(a, b)`.
- Yuvarlama kuralı tek fonksiyonda; ara sonuçlar yuvarlanmaz.
