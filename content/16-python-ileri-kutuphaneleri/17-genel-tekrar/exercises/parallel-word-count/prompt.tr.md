`top_words(texts, n)` fonksiyonunu yaz: her metnin kelimelerini
`ThreadPoolExecutor` ile ayrı ayrı `Counter`'a say (`pool.map`), sayaçları
topla ve en sık `n` kelimeyi `[kelime, sayı]` listeleri olarak döndür
(`most_common`).

**Beklenen çıktı:**

```
[['a', 4], ['c', 3]]
```
