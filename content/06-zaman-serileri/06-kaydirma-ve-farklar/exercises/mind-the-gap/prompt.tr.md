`shift` ve `diff` gün değil **satır** sayıyor. Eksik günleri olan seride
bu sessizce yanlış sonuç veriyor.

**Yapman gerekenler:**

1. `sales_messy.csv` dosyasını oku, sırala ve tekrarları topla
   (`sort_index().groupby(level=0).sum()`) → `fixed`.
2. 18 Temmuz 2024 için `fixed.diff()` değerini yazdır.
3. O farkın hangi güne göre alındığını göster: `fixed` içinde 18 Temmuz'dan
   bir önceki satırın tarihini (`"%Y-%m-%d"`) yazdır.
4. Seriyi `asfreq("D")` ile takvime oturtup tekrar `diff()` al; 18 Temmuz
   değerini yazdır.
5. İki fark serisindeki `NaN` sayılarını aynı satıra yazdır (önce
   `fixed.diff()`, sonra takvime oturtulmuş olan).

**Beklenen çıktı:**

```
-59.0
2024-07-14
nan
1 14
```

İlk satırdaki -59 "düne göre değişim" gibi okunuyor ama dört gün öncesine
göre. Takvime oturtunca o fark dürüstçe `nan`. Son satırda 1 yerine 14 `NaN`
var: sekiz eksik günün kendisi, her boşluktan sonraki ilk gün ve serinin ilk
günü.
