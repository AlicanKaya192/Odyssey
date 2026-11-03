Bellekte küçük bir `users` tablosu hazır. `city_of(name)` kişinin
şehrini döndürsün, kişi yoksa `"unknown"`. Başlangıç kodu sorguyu metin
birleştirerek kuruyor ve adında `'` olan kişide bozuluyor. Sorguyu
**parametreli** yap: `conn.execute("... WHERE name = ?", (name,))`.

**Beklenen çıktı:**

```
Istanbul
Izmir
Ankara
unknown
```
