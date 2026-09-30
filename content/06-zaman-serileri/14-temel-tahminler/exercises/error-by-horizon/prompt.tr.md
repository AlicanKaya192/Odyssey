Tahmin ufku uzadıkça hatanın nasıl büyüdüğünü iki seride ölç.

**Yapman gerekenler:**

1. Hisse fiyatında naif tahminin `h` adım sonraki hatası
   `(k.shift(-h) - k).abs().mean()`. Bunu `h = 1, 5, 10, 20, 40` için
   hesapla ve iki ondalığa yuvarlayıp liste olarak yazdır.
2. 40 günlük hatanın 1 günlük hataya oranını ve `40 ** 0.5` değerini bir
   ondalığa yuvarlayıp aynı satıra yazdır.
3. Günlük satışta mevsimsel naifin `w` hafta sonraki hatası
   `(s - s.shift(7 * w)).abs().mean()`. Bunu `w = 1, 2, 4, 8` için hesapla ve
   bir ondalığa yuvarlayıp liste olarak yazdır.
4. Günlük satışta **düz** naifin 1, 3 ve 7 gün sonraki hatasını
   (`(s - s.shift(h)).abs().mean()`) bir ondalığa yuvarlayıp liste olarak
   yazdır.

**Beklenen çıktı:**

```
[1.83, 4.5, 6.42, 8.76, 12.16]
6.7 6.3
[13.4, 14.4, 17.5, 22.9]
[36.8, 70.3, 13.4]
```

Hisse fiyatında hata ufukla büyüyor ama 40 kat uzak ufukta yalnızca 6–7 kat:
karekök büyümesi. Satışta mevsimsel naifin hatası haftadan haftaya yavaşça
artıyor. Son satır şaşırtıcı: düz naifte 7 gün sonrasının hatası, 3 gün
sonrasından çok **küçük**. Yedi gün sonrası yine aynı haftanın günü; mevsimli
seride "yakın" olan takvimde komşu gün değil, desendeki aynı konum.
