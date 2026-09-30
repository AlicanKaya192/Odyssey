`stock_price.csv` bir hissenin günlük kapanış fiyatı (`date`, `close`).
Test çağırmadan, seriyi ikiye bölerek durağan olup olmadığına bak.

Fiyat başlangıç kodunda `k` olarak okunuyor.

**Yapman gerekenler:**

1. `halves(x)` adında bir fonksiyon yaz: seriyi ortadan ikiye bölsün
   (`half = len(x) // 2`, `x.iloc[:half]` ve `x.iloc[half:]`) ve dört sayıyı
   iki ondalığa yuvarlayıp **demet** olarak döndürsün: ilk yarının ortalaması,
   ikinci yarının ortalaması, ilk yarının standart sapması, ikinci yarının
   standart sapması. Sayıları `float(...)` ile düz sayıya çevir.
2. `halves(k)` sonucunu yazdır.
3. Günlük değişimi hesapla (`k.diff().dropna()`) ve `halves` sonucunu yazdır.

**Beklenen çıktı:**

```
(119.75, 144.06, 10.01, 17.66)
(0.02, 0.15, 2.14, 2.4)
```

Fiyatta ortalama 120'den 144'e, standart sapma 10'dan 18'e çıkmış: durağan
değil. Değişim serisinde iki yarı neredeyse aynı: durağan.
