Fiyat serisinin bir rastgele yürüyüş gibi davrandığını üç ölçümle göster.

**Yapman gerekenler:**

1. Fiyatın bir gün önceki hâliyle korelasyonunu (dört ondalık) ve günlük
   değişimin bir gün önceki değişimle korelasyonunu (üç ondalık) aynı satıra
   yazdır.
2. İki basit tahmini karşılaştır. **Naif tahmin:** yarın = bugün
   (`k.shift(1)`). **Ortalama tahmini:** yarın = son 20 günün ortalaması
   (`k.shift(1).rolling(20).mean()`). İkisini ve gerçek değeri tek tabloda
   topla, `dropna()` ile ikisinin de dolu olduğu günlere in ve her tahminin
   ortalama mutlak hatasını iki ondalığa yuvarlayıp aynı satıra yazdır (önce
   naif).
3. Artış günlerinin oranını hesapla (`(change > 0).mean()`). Sonra yalnızca
   **bir önceki gün artış olan** günlerde aynı oranı hesapla. İkisini üç
   ondalığa yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
0.9927 0.041
1.84 5.36
0.529 0.53
```

Düzey dünü neredeyse birebir taşıyor, değişimler arasında ise ilişki yok. Naif
tahmin, 20 günlük ortalamadan belirgin biçimde iyi: rastgele yürüyüşte en
taze bilgi son değer. Ve dün artmış olması bugünün artma olasılığını neredeyse
hiç değiştirmiyor.
