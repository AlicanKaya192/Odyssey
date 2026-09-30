Çok adımlı bir tahmin için aralığı, kayan başlangıçtaki **gerçek
hatalardan** kur: her ufuk haftasının kendi yüzdelikleriyle.

Başlangıç kodunda `snaive(train, h)` ve `cuts` (13 kesim) hazır.

**Yapman gerekenler:**

1. Her kesimde 28 günlük mevsimsel naif tahminin hatasını
   (`gerçek − tahmin`) hesapla; 13 × 28'lik bir numpy dizisinde topla.
2. İlk 9 deneyi aralığı **kurmak**, son 4 deneyi **sınamak** için ayır.
3. İlk 9 deneyin hatalarından, ufkun her haftası için (sütunlar 0–6, 7–13,
   14–20, 21–27) %10 ve %90 yüzdeliklerini hesapla; bir ondalıkla
   `hafta alt üst` biçiminde dört satır yazdır.
4. Aynı haftalar için son 4 deneyde hataların bu sınırlar içinde kalma oranını
   iki ondalıkla liste olarak yazdır.
5. Son 4 deneyin toplam kapsamasını üç ondalıkla yazdır.

**Beklenen çıktı:**

```
1 -28.8 24.8
2 -37.0 15.8
3 -25.8 21.6
4 -32.8 18.8
[0.93, 0.54, 0.64, 0.54]
0.661
```

İlk hafta için aralık tutuyor; sonraki haftalarda %80 dediği aralık yarı
yarıya kaçırıyor. Neden? Son dört deney sonbahar ve yıl sonu: satışlar yükseliyor
ve hatalar artı yöne kayıyor. İlk dokuz deneyin hataları bu dönemi temsil etmiyor.
Deneysel aralık varsayımsız ama **büyülü değil**: geçmiş hatalar geleceğe
benzediği ölçüde çalışır. Kaçan değerlerin hepsi üst sınırın üstünde, alt
sınırın altında tek bir gün yok: aralık dar değil, **kaymış**.
