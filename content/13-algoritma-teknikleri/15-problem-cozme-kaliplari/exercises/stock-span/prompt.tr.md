`stock_span(prices)` fonksiyonunu yaz: her gün için, o gün dahil geriye
doğru fiyatı bugünkünden **büyük olmayan** ardışık gün sayısını döndürsün
(`[100, 80, 60, 70, 60, 75, 85]` → `[1, 1, 1, 2, 1, 4, 6]`).

Monoton yığın: yığında fiyatları azalan günlerin indeksleri. Bugünkü fiyattan
küçük ya da eşit olanları çıkar; kalan tepedeki gün, aralığın sınırı. Son
satırda yüz bin gün sürekli artıyor.

**Beklenen çıktı:**

```
[1, 1, 1, 2, 1, 4, 6]
100000
```
