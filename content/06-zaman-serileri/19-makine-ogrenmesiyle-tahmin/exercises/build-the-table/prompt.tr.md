Günlük satış serisini bir özellik tablosuna çevir.

**Yapman gerekenler:**

1. `features(y)` fonksiyonunu yaz; indeksi `y.index` olan bir tablo döndürsün:
   - `lag1`, `lag2`, `lag7`, `lag14`: `y.shift(k)`
   - `mean7`: `y.shift(1).rolling(7).mean()`
   - `mean28`: `y.shift(1).rolling(28).mean()`
   - `dow`: haftanın günü, `month`: ay
2. `features(s)` tablosuna hedefi `y` sütunu olarak ekle
   (`.join(s.rename("y"))`) ve `dropna()` uygula. Şeklini ve ilk tarihini aynı
   satıra yazdır.
3. Sütun adlarını liste olarak yazdır.
4. 10 Mart 2024 satırını denetle: o günün `y` değerini, `lag1`, `lag7` ve
   `mean7` değerlerini (son ikisi tam sayı, `mean7` bir ondalık) aynı satıra
   yazdır.
5. Aynı `mean7` değerini elle hesapla: 3–9 Mart 2024 satışlarının ortalaması
   (bir ondalık).

**Beklenen çıktı:**

```
(1068, 9) 2022-01-29
['lag1', 'lag2', 'lag7', 'lag14', 'mean7', 'mean28', 'dow', 'month', 'y']
311 384 319 283.7
283.7
```

Son iki satırdaki `mean7` aynı: 10 Mart'ın özelliği, 3–9 Mart'ı kapsıyor;
10 Mart'ın kendisi içinde **yok**. `shift(1)` tam olarak bunu sağlıyor. Tablo
28 satır kısaldı: `mean28` için geçmiş yetmediği günler.
