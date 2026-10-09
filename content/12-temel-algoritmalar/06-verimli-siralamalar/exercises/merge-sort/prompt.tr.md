`merge_sort(items)` fonksiyonunu **özyinelemeyle** yaz: listenin sıralı
bir kopyasını döndürsün. Birleştirme fonksiyonu (`merge`) hazır.

1. Temel durum: 0 ya da 1 elemanlı liste zaten sıralı.
2. Ortadan ikiye böl: `items[:mid]` ve `items[mid:]`.
3. Her yarıyı `merge_sort` ile sırala ve `merge` ile birleştir.

`sorted` ve `.sort()` kullanma.

**Beklenen çıktı:**

```
[3, 9, 10, 27, 38, 43, 82]
[]
```
