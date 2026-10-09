`min_coins(amount, coins)` fonksiyonunu **tablo doldurarak** yaz: tutarı
vermek için gereken en az para sayısını döndürsün; verilemiyorsa `-1`.

- `best = [0] + [inf] * amount`
- her `a` için her `c <= a` parasında `best[a − c] + 1` daha küçükse güncelle
- sonda `best[amount]` hâlâ `inf` ise `-1`

**Beklenen çıktı:**

```
2
4
-1
51
```
