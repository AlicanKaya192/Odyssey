`backoff(n, base, cap)` fonksiyonunu yaz: üstel beklemede ilk `n`
denemenin bekleme sürelerini liste olarak döndürsün. `i`. süre
`base * 2 ** i` (i 0'dan başlar), ama hiçbiri `cap`'i geçmesin.
Örnek: `backoff(5, 1, 10)` → `[1, 2, 4, 8, 10]`.

**Beklenen çıktı:**

```
[1, 2, 4, 8, 10]
[0.5, 1.0, 2.0, 4.0]
```
