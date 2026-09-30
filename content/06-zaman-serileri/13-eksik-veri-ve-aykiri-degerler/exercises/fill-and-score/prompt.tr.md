Eksik 8 günün gerçek değerleri `store_sales.csv` dosyasında duruyor. Dört
doldurma yöntemini dene ve hangisinin gerçeğe ne kadar yaklaştığını ölç.

Başlangıç kodunda `full` (eksikleri `NaN` olan 2024 serisi) ve `truth` (gerçek
satış) hazır.

**Yapman gerekenler:**

1. Eksik günlerin indeksini al: `days = full[full.isna()].index`.
2. `score(filled)` adında bir fonksiyon yaz: doldurulmuş serinin eksik
   günlerdeki değerleri ile gerçek değerler arasındaki ortalama mutlak farkı
   bir ondalığa yuvarlayıp döndürsün.
3. Dört yöntemi uygula ve `ad hata` biçiminde alt alta yazdır:
   - `ffill`: `full.ffill()`
   - `linear`: `full.interpolate()`
   - `week ago`: `full.fillna(full.shift(7))`
   - `both sides`: bir hafta öncesi ile sonrasının ortalaması
     (`pd.concat([full.shift(7), full.shift(-7)], axis=1).mean(axis=1)`)
4. 10 Şubat için gerçek değeri ve dört yöntemin yazdığı değeri tam sayıya
   yuvarlayıp aynı satıra yazdır (sıra: gerçek, ffill, linear, week ago, both
   sides).

**Beklenen çıktı:**

```
ffill 45.0
linear 46.1
week ago 9.8
both sides 7.0
388 302 276 389 382
```

Haftalık deseni kullanan iki yöntem, kullanmayanlardan beş kat daha isabetli.
Son satır nedenini gösteriyor: 10 Şubat bir cumartesi; `ffill` ve doğrusal
doldurma hafta içi düzeyinde bir sayı yazıyor.
