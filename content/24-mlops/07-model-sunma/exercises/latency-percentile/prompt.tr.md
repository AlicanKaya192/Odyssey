Dersteki `percentile(values, p)` fonksiyonunu sıra yöntemiyle (nearest rank) yaz ve iki uç durumu ekle:

- Değerleri sırala; `rank = ceil(p / 100 * len(values))`; sıralı listenin `rank`'inci elemanını döndür (1'den sayarak).
- `p` 0 ise `rank` 0 olur: o zaman ilk elemanı döndür.
- Liste boşsa `None` döndür.

**Beklenen çıktı:**

```
p50: 13
p95: 90
p99: 250
empty: None
```
