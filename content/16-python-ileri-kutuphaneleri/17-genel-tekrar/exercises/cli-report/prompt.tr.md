`report(argv)` fonksiyonunu yaz:

- `argparse` ile `--min` (`type=Decimal`, varsayılan `Decimal("0")`) ve
  isteğe bağlı `--customer` tanımla.
- Bellekte bir SQLite tablosu `orders (id INTEGER PRIMARY KEY, customer TEXT,
  total TEXT)` kur ve `ORDERS`'ı `executemany` ile ekle.
- Satırları al; tutarı `Decimal`'a çevirip `--min`'den küçük olanları ve
  (verildiyse) başka müşterininkileri at.
- `[id, "tutar"]` listelerini id sırasıyla döndür. Müşteri süzgecini SQL'de
  `?` ile yapabilirsin.

**Beklenen çıktı:**

```
[[1, '19.99'], [3, '12.50'], [4, '40.00']]
[[1, '19.99'], [3, '12.50']]
```
