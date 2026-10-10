Talep `1000 - 8 * fiyat`, kâr `(fiyat - cost) * talep`. `best_price(cost,
max_price)` kârı **en büyük** yapan fiyatı `minimize_scalar` ile
(`bounds=(cost, max_price)`, `method="bounded"`) bulsun ve `[fiyat, kâr]`
döndürsün (2 ve 1 basamak). Başlangıç kodu kârın kendisini en küçüklüyor.

**Beklenen çıktı:**

```
[72.5, 22050.0]
[82.5, 14450.0]
```
