Bu alıştırma bir **grafik yalanını** gösteriyor.

**Yapman gerekenler:**

1. Şehirleri ve notları gösteren bir çubuk grafik çiz.
2. Eksenin alt sınırının sıfır olup olmadığını yazdır (`True` ya da
   `False`).
3. Ekseni **0 ile 100 arasına** zorla.
4. Yeni alt ve üst sınırı **yan yana**, tam sayı olarak yazdır.

**Beklenen çıktı:**

```
True
0 100
```

**Bu veride eksen zaten sıfırdan başlıyor** — çünkü değerler 69 ile 87
arasında ve matplotlib sıfırı makul buluyor.

Ama değerler 85, 87 ve 88 olsaydı eksen 84'ten başlayabilirdi ve aradaki
%3'lük fark ekranda **üç kat** gibi görünürdü.

**Kural:** çubuk grafikte ekseni sıfırdan başlat. Sebebi şu: çubuğun
**uzunluğu** değeri temsil ediyor. Alt kısmı kesersen uzunluk artık değerle
orantılı olmuyor ve grafik yalan söylüyor.

Çizgi grafiklerinde bu kural yok — orada konu eğilim, mutlak büyüklük değil.
