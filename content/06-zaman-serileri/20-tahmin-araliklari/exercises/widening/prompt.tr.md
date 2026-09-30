Hisse fiyatında naif tahminin aralığı ufukla nasıl genişlemeli? Karekök
kuralını ve sabit genişliği karşılaştır.

**Yapman gerekenler:**

1. Günlük değişimin standart sapmasını hesapla: `sd = k.diff().std()`; üç
   ondalıkla yazdır.
2. Serinin son değerinden başlayarak `h = 1, 10, 40` için %95'lik aralığı
   (`son ± 1.96 * sd * sqrt(h)`) bir ondalıkla `h alt üst` biçiminde alt alta
   yazdır.
3. `coverage(h, widen)` fonksiyonunu yaz: serinin **bütün** günlerinden
   başlayarak `h` gün sonraki hatayı al (`(k.shift(-h) - k).dropna()`);
   `widen` doğruysa sınır `1.96 * sd * sqrt(h)`, değilse `1.96 * sd`; mutlak
   hatanın sınırın içinde kalma oranını üç ondalıkla döndürsün.
4. `h = 1, 10, 40` için iki kapsamayı `h karekök sabit` biçiminde alt alta
   yazdır.

**Beklenen çıktı:**

```
2.276
1 162.0 170.9
10 152.3 180.5
40 138.2 194.7
1 0.953 0.953
10 0.925 0.411
40 0.969 0.19
```

Karekök kuralıyla kapsama üç ufukta da %95'in yakınında. Sabit genişlik yalnızca
bir gün için doğru; 40 günlük ufukta "%95" dediği aralık gerçeği beşte bir
oranında tutuyor. Aralığın genişliği de ufkun bir fonksiyonu.
