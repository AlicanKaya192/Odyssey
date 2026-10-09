`power(base, exp)` fonksiyonunu **özyinelemeyle** yaz: `base`'in `exp`'inci
kuvvetini döndürsün (`exp >= 0` tam sayı).

- `power(2, 10)` → `1024`
- `power(5, 0)` → `1`

**Kurallar:** `**` işlecini, `pow` fonksiyonunu ve döngüyü kullanma.
Temel durum `exp == 0`; adım `base * power(base, exp - 1)`.

**Beklenen çıktı:**

```
1024
1
81
```
