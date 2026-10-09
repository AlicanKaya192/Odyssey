`bloom_check(items, queries, bits, hashes)` fonksiyonunu yaz: `bits`
uzunlukta bir Bloom filtresi kur (`bytearray(bits)`), `items`'ı ekle ve her
sorgu için "muhtemelen var" ise `True`, "kesinlikle yok" ise `False` içeren
listeyi döndürsün.

Öğenin konumları: `s = 0..hashes − 1` için `h(item, s) % bits`. `h` hazır.

**Beklenen çıktı:**

```
[True, True, False]
15
```
