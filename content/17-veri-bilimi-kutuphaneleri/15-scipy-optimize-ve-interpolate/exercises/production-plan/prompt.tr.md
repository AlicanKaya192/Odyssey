`plan(profits, hours, limits)` ürün başına kârı (`profits`), her makinede ürün
başına saati (`hours[makine][ürün]`) ve makine saat sınırlarını (`limits`)
alsın. Kârı **en büyük** yapan üretimi `optimize.linprog` ile bulsun (adetler
0 ya da daha büyük). `{"units": adetler, "profit": kâr}` döndürsün (adetler
2, kâr 1 basamak). `linprog` en küçükler: kârların eksisini ver.

**Beklenen çıktı:**

```
[25.0, 7.5] 1125.0
```
