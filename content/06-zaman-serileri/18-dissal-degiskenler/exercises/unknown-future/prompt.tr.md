Kampanya ve tatil takvimi önceden belli; sıcaklık değil. 31 Ekim'de
durduğunu düşün ve Kasım sıcaklığı için üç farklı varsayımla tahmin yap.

Başlangıç kodunda `train`, `test`, `columns` ve kurulmuş model `fit` hazır.

**Yapman gerekenler:**

1. Üç gelecek tablosu kur. Üçünde de `promo` ve `holiday` test dönemindeki
   gerçek değerler (takvim belli); fark yalnızca `temp_c` sütununda:
   - `"actual"`: testteki gerçek sıcaklık (hile)
   - `"last"`: eğitimin son günündeki sıcaklık, 28 gün boyunca
   - `"normal"`: mevsim normali: eğitim verisinde o takvim gününün
     (`dayofyear`) ortalama sıcaklığı
2. Her varsayımın **sıcaklık** hatasını (testteki gerçek sıcaklığa göre
   ortalama mutlak fark, bir ondalık) `ad hata` biçiminde alt alta yazdır.
3. Her varsayımla **satış** tahmini yap ve ortalama mutlak hatayı iki
   ondalıkla `ad MAE` biçiminde alt alta yazdır.
4. "Gerçek sıcaklık" sonucunun dürüst sonuçların en iyisinden ne kadar iyi
   olduğunu iki ondalıkla yazdır (dürüst en iyi MAE eksi hileli MAE).

**Beklenen çıktı:**

```
actual 0.0
last 1.5
normal 2.2
actual 11.07
last 12.5
normal 15.59
1.43
```

Gerçek sıcaklıkla bulunan sonuç bir tavan: 31 Ekim'de o ölçümler yoktu. Bu
28 günde "son değer" mevsim normalinden iyi çıktı, çünkü Kasım sıcaklığı
tesadüfen Ekim sonundaki değerin etrafında kaldı. Dersteki 13 deneylik
sınamada sıra tersine: mevsim normali 15.0, son değer 17.7. Tek bir dönem
yanıltır; hangi vekilin iyi olduğuna da kayan başlangıçla karar verilir.
