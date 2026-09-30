Aylık yolcu serisini iki modelle de ayrıştır ve hangisinin doğru olduğunu
kalıntıya sor.

**Yapman gerekenler:**

1. `add = seasonal_decompose(p, model="additive", period=12)` ve
   `mul = seasonal_decompose(p, model="multiplicative", period=12)`.
2. Toplamsal kalıntının mutlak değerinin **yıla göre** ortalamasını al;
   2013, 2019 ve 2023 değerlerini bir ondalığa yuvarlayıp aynı satıra yazdır.
3. Toplamsal kalıntının 2013 ve 2023 **Temmuz** değerlerini (bir ondalık)
   aynı satıra yazdır.
4. Çarpımsal kalıntı 1'in etrafında bir oran. Yüzde sapmaya çevir:
   `pct = (mul.resid - 1).abs() * 100`. Aynı üç yılın ortalamasını bir
   ondalığa yuvarlayıp aynı satıra yazdır.
5. `pct`'nin en büyük değerini bir ondalığa yuvarlayıp yazdır.
6. Çarpımsal mevsim çarpanlarının en küçüğünü ve en büyüğünü, ay numarasıyla
   birlikte `ay çarpan ay çarpan` biçiminde yazdır (üç ondalık). Çarpanlar
   `mul.seasonal.iloc[:12]` içinde, Ocak'tan Aralık'a.

**Beklenen çıktı:**

```
12.7 2.8 13.1
-22.0 20.5
0.6 0.7 1.4
3.6
2 0.83 8 1.255
```

Toplamsal modelin kalıntısı uçlarda büyük, ortada küçük ve Temmuz'da işareti
eksiden artıya dönüyor: tek bir sabit "Temmuz payı" ilk yıllar için fazla, son
yıllar için az. Çarpımsal modelde sapma her yıl %1 dolayında. Seri çarpımsal.
