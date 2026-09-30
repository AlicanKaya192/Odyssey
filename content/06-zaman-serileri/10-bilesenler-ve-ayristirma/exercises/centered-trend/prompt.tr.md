Klasik ayrıştırmanın ilk adımını elle yap: haftalık deseni götüren 7 günlük
**ortalanmış** hareketli ortalama.

Seri başlangıç kodunda okunuyor (`s`, günlük, 1096 gün).

**Yapman gerekenler:**

1. `trend = s.rolling(7, center=True).mean()` hesapla.
2. Trenddeki `NaN` sayısını yazdır.
3. Trendin dolu olduğu ilk ve son tarihi aynı satıra yazdır (`.date()`).
4. O iki tarihteki trend değerini bir ondalığa yuvarlayıp aynı satıra yazdır.
5. Karşılaştırma için geriye dönük ortalamayı da hesapla:
   `trailing = s.rolling(7).mean()`. Ortalanmış trendin 25 Aralık 2024
   değerini ve geriye dönük ortalamanın 28 Aralık 2024 değerini (bir ondalık)
   aynı satıra yazdır.

**Beklenen çıktı:**

```
6
2022-01-04 2024-12-28
230.1 393.3
386.1 386.1
```

Son satırdaki iki sayı aynı: ikisi de 22–28 Aralık günlerinin ortalaması.
Ortalanmış pencere bu ortalamayı haftanın **ortasına** (25'ine), geriye dönük
pencere **sonuna** (28'ine) yazıyor. Ayrıştırmada doğru yer ortası; bedeli iki
uçta üçer günlük boşluk.
