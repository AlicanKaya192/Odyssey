Önbellek anahtarları `"müşteri@sürüm"` biçiminde (`"C1@v2"`). Canlı model değişince eskiyen kayıtları bulan `stale_keys(keys, live_version)` fonksiyonunu yaz:

- Her anahtarı `"@"` ile müşteri ve sürüm olarak ayır.
- Sürümü `live_version` olmayanların **müşterilerini** sırayla döndür.

**Beklenen çıktı:**

```
['C1', 'C3']
['C2', 'C4']
[]
```
