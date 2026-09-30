Aynı 28 günlük deneyi iki farklı başlangıçtan yap ve mevsimsel naifin
hatasının **yönüne** bak.

Başlangıç kodunda `snaive(train, h)` fonksiyonu hazır: son haftayı `h` gün
boyunca tekrarlayan bir liste döndürüyor.

**Yapman gerekenler:**

1. `evaluate(cut)` adında bir fonksiyon yaz: `cut` tarihine kadar olan veri
   eğitim, sonraki 28 gün test. Mevsimsel naif tahmini kur ve üç şeyi demet
   olarak döndür: ortalama mutlak hata (iki ondalık), yanlılık (iki ondalık),
   tahminin **düşük kaldığı** gün sayısı (`error > 0`).
2. `evaluate("2024-11-05")` ve `evaluate("2024-12-03")` sonuçlarını alt alta
   yazdır.
3. İkinci deney için (3 Aralık) hatanın haftalara göre ortalamasını yazdır:
   28 günlük hatayı 7'şerlik dört parçaya böl ve her parçanın ortalamasını
   bir ondalığa yuvarlayıp liste olarak yazdır.

**Beklenen çıktı:**

```
(11.64, 6.79, 20)
(40.25, 40.25, 28)
[19.4, 35.0, 43.9, 62.7]
```

Kasım deneyinde yanlılık MAE'nin yarısı kadar: hatalar iki yöne dağılmış.
Aralık deneyinde MAE ile yanlılık aynı: tahmin 28 günün hepsinde düşük. Son
satır nedenini gösteriyor: hata haftadan haftaya büyüyor. Yıl sonu tırmanışı
sürerken tahmin Kasım sonunun düzeyinde kalıyor.
