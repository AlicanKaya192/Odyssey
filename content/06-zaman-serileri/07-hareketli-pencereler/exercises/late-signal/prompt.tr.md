Aynı 28 günlük ortalama, iki yerleşim: geriye dönük ve ortalanmış. Yıl
sonu tepesini hangisi ne zaman gösteriyor?

**Yapman gerekenler:**

1. Dosyayı oku. İki seri hesapla: `s.rolling(28).mean()` ve
   `s.rolling(28, center=True).mean()`.
2. 15 Kasım 2023 – 15 Şubat 2024 aralığında her birinin en yüksek olduğu
   tarihi (`"%Y-%m-%d"`) alt alta yazdır: önce ortalanmış, sonra geriye
   dönük.
3. İki tarih arasındaki farkı gün olarak yazdır.
4. İki tepenin değerini bir ondalığa yuvarlayıp aynı satıra yazdır.
5. Serinin **son 14 gününde** her birinde kaç `NaN` olduğunu aynı satıra
   yazdır: önce ortalanmış, sonra geriye dönük.

**Beklenen çıktı:**

```
2023-12-19
2024-01-01
13
330.9 330.9
13 0
```

Tepenin yüksekliği aynı, tarihi 13 gün farklı: geriye dönük ortalama aynı
eğrinin sağa kaymış hâli. Son satır ortalanmış pencerenin bedelini gösteriyor:
serinin en güncel günleri için değer yok, çünkü o günlerin "sonrası" henüz
yaşanmadı.
