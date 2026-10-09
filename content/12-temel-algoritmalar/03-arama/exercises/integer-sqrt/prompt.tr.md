`integer_sqrt(n)` fonksiyonunu **cevap üzerinde ikili aramayla** yaz:
`k * k <= n` olan **en büyük** `k`'yi döndürsün (`n >= 0`).

- `integer_sqrt(50)` → `7` (`7 * 7 = 49`, `8 * 8 = 64`)
- `integer_sqrt(0)` → `0`

**Fikir:** cevap `0` ile `n` arasında. `k` büyüdükçe `k * k <= n` önce
doğru, sonra hep yanlış. Aralığın ortasını dene: koşul doğruysa cevap ya bu
ya daha büyüğü (`answer = mid`, `lo = mid + 1`); yanlışsa daha küçüğü
(`hi = mid - 1`).

**Kurallar:** `math.sqrt`, `math.isqrt` ve `** 0.5` kullanma.

**Beklenen çıktı:**

```
0 0
1 1
15 3
16 4
50 7
99 9
1000000
```

Son satırdaki dev sayı için bile yaklaşık 40 tur yetiyor.
