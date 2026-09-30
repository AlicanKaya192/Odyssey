Mevsimsel naif tahmini bir yüzdelik tahminine çevir ve pinball kaybıyla
ölç.

Başlangıç kodunda `past` (2023 hataları), `base` (2024 için mevsimsel naif
tahmin) ve `actual` (2024 gerçek değerleri) hazır.

**Yapman gerekenler:**

1. `pinball(actual, forecast, q)` fonksiyonunu yaz:
   `diff = actual - forecast`; sonuç `np.maximum(q * diff, (q - 1) * diff)`
   değerlerinin ortalaması.
2. `q = 0.5, 0.8, 0.9, 0.95` için:
   - eklenecek pay: `past.quantile(q)`
   - yüzdelik tahmini: `base + pay`
   - bu tahminin pinball kaybı
   - gerçek değerin tahminin **altında ya da ona eşit** kaldığı günlerin oranı

   Her `q` için `q pay kayıp oran` biçiminde bir satır yazdır (pay bir, kayıp
   iki, oran üç ondalık).
3. Karşılaştırma için: `q = 0.9` iken **nokta tahminin** (`base`) pinball
   kaybını iki ondalıkla yazdır.

**Beklenen çıktı:**

```
0.5 2.0 6.92 0.514
0.8 16.0 4.68 0.801
0.9 23.0 2.84 0.913
0.95 28.0 1.68 0.962
7.3
```

Son sütun söylenen yüzdeliğe çok yakın: 0.9 yüzdeliği günlerin %91'inde
gerçeğin üstünde kaldı. Son satır, nokta tahminini %90 sınırı diye kullanmanın
bedelini gösteriyor: pinball kaybı iki buçuk katı. Aynı tahmin, farklı soru;
farklı soruya farklı sayı gerekir.
