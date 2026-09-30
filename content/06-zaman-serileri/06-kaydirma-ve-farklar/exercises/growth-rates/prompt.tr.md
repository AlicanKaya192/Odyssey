Aynı soru, iki farklı karşılaştırma: bir önceki aya göre ve geçen yılın
aynı ayına göre.

**Yapman gerekenler:**

1. Dosyayı oku ve her ayın **günlük ortalamasını** hesapla:
   `s.resample("ME").mean()`. (Toplam yerine ortalama: ay uzunluğu
   karışmasın.)
2. Aydan aya yüzde değişimi (`pct_change() * 100`) 2024'ün ilk dört ayı için
   bir ondalığa yuvarlayıp liste olarak yazdır.
3. Yıldan yıla yüzde değişimi (`pct_change(12) * 100`) aynı dört ay için
   liste olarak yazdır.
4. 2024'ün on iki ayının yıldan yıla değişimlerinin ortalamasını bir
   ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
[-11.5, -0.3, -1.7, -7.3]
[11.9, 12.8, 16.4, 10.5]
13.0
```

İlk satıra bakan "satışlar düşüyor" der; ikinci satıra bakan "yılda %10'dan
fazla büyüyoruz" der. Aydan aya düşüş, Aralık tepesinden sonra her yıl
görülen mevsimsellik.
