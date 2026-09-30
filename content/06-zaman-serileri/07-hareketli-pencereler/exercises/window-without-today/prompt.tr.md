Bugünün satışını tahmin edecek bir modelin girdisi bugünün satışını
içeremez. İki özelliği karşılaştır.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `s` serisi olarak oku.
2. İki özellik kur: `naive = s.rolling(7).mean()` ve
   `safe = s.shift(1).rolling(7).mean()`.
3. 9 Mart 2024 için ikisini bir ondalığa yuvarlayıp aynı satıra yazdır.
4. Aynı iki sayıyı elle doğrula: 3–9 Mart ortalamasını ve 2–8 Mart
   ortalamasını bir ondalığa yuvarlayıp aynı satıra yazdır.
5. `safe` serisinde baştan kaç `NaN` olduğunu yazdır.
6. 7 gün ileriyi tahmin edecek bir model için aynı özelliği kur
   (`s.shift(7).rolling(7).mean()`) ve 9 Mart 2024 değerini bir ondalığa
   yuvarlayıp yazdır.

**Beklenen çıktı:**

```
283.7 282.0
283.7 282.0
7
283.1
```

`naive` penceresi 9 Mart'ı da içeriyor; `safe` 8 Mart'ta bitiyor. Yedi gün
ileriyi tahmin edeceksen tahmin anında bilinen son değer yedi gün önceki;
pencere de orada bitmeli.
