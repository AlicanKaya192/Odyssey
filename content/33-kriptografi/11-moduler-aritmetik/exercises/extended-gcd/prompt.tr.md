`egcd(a, b)` `[g, x, y]` döndürsün: `g = gcd(a, b)` ve
`a * x + b * y == g`. Özyinelemeli: `b == 0` ise `a = a * 1 + 0 * 0`
olduğundan taban durum `[a, 1, 0]`'dır. Başlangıç kodunun taban durumu
yanlış.

**Beklenen çıktı:**

```
1 4 -1
1
2 2
```
