## İşlemler

| İşlem | Python | Örnek | Sonuç |
|---|---|---|---|
| Kalan | `a % n` | `27 % 12` | 3 |
| Mod içinde toplama | `(a + b) % n` | `(10 + 5) % 12` | 3 |
| Mod içinde çarpma | `(a * b) % n` | `(7 * 8) % 12` | 8 |
| Büyük üs | `pow(a, e, n)` | `pow(7, 128, 13)` | 3 |
| Ebob | `math.gcd(a, b)` | `math.gcd(12, 18)` | 6 |
| Ters | `pow(a, -1, n)` | `pow(3, -1, 11)` | 4 |

## Kurallar

- Python'da `a % n` her zaman `0` ile `n - 1` arasındadır (eksi `a`'da da).
- Ara adımlarda `% n` almak sonucu değiştirmez; sayılar küçük kalır.
- `a ** e % n` yerine **her zaman** `pow(a, e, n)`: aynı sonuç, çok daha hızlı.
- Ters yalnızca `gcd(a, n) == 1` ise vardır; yoksa `pow` `ValueError` verir.

## Kare al ve çarp

```text
sonuç = 1
üs > 0 iken:
    üssün son ikili basamağı 1 ise: sonuç = sonuç × taban mod n
    taban = taban × taban mod n
    üssü bir basamak sağa kaydır
```

Tur sayısı üssün **ikili basamak sayısı** kadardır (117 için 7).

## Genişletilmiş Öklid

`egcd(a, b)` → `(g, x, y)`, öyle ki `a·x + b·y = g`. `g == 1` ise
`x % b`, `a`'nın mod `b`'deki tersidir.

## Fermat'nın küçük teoremi

`p` asal ve `a % p != 0` ise `pow(a, p - 1, p) == 1`.
